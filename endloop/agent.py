import os
import logging
import json
import re
from openai import OpenAI
from typing import Optional, List, Dict, Any

from .memory import StateBuffer
from .tools import EndLoopTool
from .prompts import DEFAULT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

REACT_INSTRUCTIONS = """
You are operating in an advanced ReAct (Reason+Act) Loop with Endogenous Pruning.
You must structure your response strictly in the following phases:

[Pensamiento Interno]: You must list two possible approaches, and explicitly state why you discard one of them based on the context.
[Acción]: The exact tool name you want to call.
[Parámetros]: A valid JSON object with the parameters for the tool.
[Espera de Observación]: Stop generating after the parameters.

If you have completed the task and no more tools are needed, use the action "FINISH" and provide the final payload in the parameters as {"payload": "..."}.
"""

class EndLoopAgent:
    """
    EndLoop ReAct Agent Framework with Metacognitive Memory and Endogenous Pruning.
    """
    def __init__(
        self,
        tools: List[EndLoopTool],
        model: str = "gpt-4o",
        max_iterations: int = 10,
        client: Optional[OpenAI] = None
    ):
        self.model = model
        self.max_iterations = max_iterations
        self.tools = {tool.name: tool for tool in tools}
        self.memory = StateBuffer()
        self.client = client or OpenAI(api_key=os.environ.get("LLM_API_KEY"))

    def _get_system_prompt(self):
        tool_desc = "\n".join([f"- {t.name}: {t.description}" for t in self.tools.values()])
        return f"{DEFAULT_SYSTEM_PROMPT}\n\n{REACT_INSTRUCTIONS}\n\nAvailable Tools:\n{tool_desc}\n- FINISH: Use to end execution and return the final payload."

    def _summarize_history(self, history_text: str) -> str:
        """Triggered Compression (Metacognitive Compression)"""
        prompt = f"Summarize the following execution history. Extract the key findings and progress made so far:\n\n{history_text}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content

    def _parse_react_output(self, text: str) -> Dict[str, Any]:
        """Very basic parsing of the ReAct format."""
        action_match = re.search(r"\[Acción\]:\s*(.+)", text)
        params_match = re.search(r"\[Parámetros\]:\s*(\{.*\})", text, re.DOTALL)
        
        action = action_match.group(1).strip() if action_match else "UNKNOWN"
        params_str = params_match.group(1).strip() if params_match else "{}"
        
        try:
            params = json.loads(params_str)
        except json.JSONDecodeError:
            params = {}
            
        return {"action": action, "parameters": params}

    def run(self, user_task: str) -> str:
        self.memory.set_goal(user_task)
        
        for iteration in range(self.max_iterations):
            if self.memory.needs_compression():
                logger.info("[EndLoop Memory] Triggering context compression...")
                self.memory.compress_history(self._summarize_history)

            messages = [
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": self.memory.get_system_context()}
            ]
            
            # Append current history
            messages.extend(self.memory.history)
            
            # Generate next step
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                stop=["[Espera de Observación]"]
            )
            
            agent_output = response.choices[0].message.content
            self.memory.add_message("assistant", agent_output)
            
            parsed = self._parse_react_output(agent_output)
            action = parsed.get("action")
            params = parsed.get("parameters", {})
            
            if action == "FINISH":
                return params.get("payload", "Task Completed")
                
            if action in self.tools:
                tool = self.tools[action]
                observation = tool.execute(**params)
                self.memory.add_message("user", f"[Observación]: {observation}")
            else:
                self.memory.add_message("user", f"[Error Observation]: Tool '{action}' not found.")
                
        raise TimeoutError("EndLoop Agent failed to finish within max iterations.")
