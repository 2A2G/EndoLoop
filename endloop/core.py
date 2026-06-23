import os
import logging
from openai import OpenAI
from typing import Optional

from .prompts import DEFAULT_SYSTEM_PROMPT, DEFAULT_AUDIT_PROMPT

logger = logging.getLogger(__name__)

class EndLoopSystem:
    """
    EndLoop State-Driven Cognition System.
    Wraps LLM execution in an autonomous audit-and-refine loop.
    """
    def __init__(self, model: str = "gpt-4o", max_loops: int = 3, client: Optional[OpenAI] = None):
        self.model = model
        self.max_loops = max_loops
        self.client = client or OpenAI(api_key=os.environ.get("LLM_API_KEY"))

    def run(self, user_task: str, initial_data: str = "") -> str:
        """
        Executes a task through the endogenous pruning loop.
        """
        messages = [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Task: {user_task}\nData: {initial_data}"}
        ]
        
        for loop_count in range(self.max_loops):
            # 1. Generate / Correct step
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.2
            )
            current_state = response.choices[0].message.content
            messages.append({"role": "assistant", "content": current_state})
            
            # 2. Inject the Floating Control Prompt
            messages.append({"role": "user", "content": DEFAULT_AUDIT_PROMPT})
            
            audit_response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.0
            )
            audit_result = audit_response.choices[0].message.content
            
            if "[STATE: APPROVED]" in audit_result:
                logger.info(f"[EndLoop] Reached optimal state after {loop_count} refinements.")
                return current_state
            else:
                # 3. Refine
                messages.pop() # Remove the trigger
                messages.append({"role": "user", "content": f"Correction required: {audit_result}"})
                logger.info(f"🔄 [EndLoop Iteration {loop_count + 1}] Self-correction triggered.")
                
        raise TimeoutError(f"EndLoop System failed to converge to an optimal state within {self.max_loops} loops.")
