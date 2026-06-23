import os
import logging
from openai import OpenAI
from typing import Optional, List

from .prompts import DEFAULT_SYSTEM_PROMPT, DEFAULT_AUDIT_PROMPT

logger = logging.getLogger(__name__)

class EndLoopSystem:
    """
    EndLoop State-Driven Cognition System.
    Wraps LLM execution in an autonomous audit-and-refine loop.
    """
    def __init__(
        self, 
        model: str = "gpt-4o", 
        max_loops: int = 3, 
        generation_temperature: float = 0.2,
        audit_temperature: float = 0.0,
        custom_checkpoints: Optional[List[str]] = None,
        client: Optional[OpenAI] = None
    ):
        self.model = model
        self.max_loops = max_loops
        self.generation_temperature = generation_temperature
        self.audit_temperature = audit_temperature
        self.custom_checkpoints = custom_checkpoints or []
        self.client = client or OpenAI(api_key=os.environ.get("LLM_API_KEY"))

    def _build_audit_prompt(self) -> str:
        prompt = DEFAULT_AUDIT_PROMPT
        if self.custom_checkpoints:
            # Safely inject custom checkpoints right before the routing section
            custom_text = "\n".join([f"- CUSTOM CHECKPOINT: {cp}" for cp in self.custom_checkpoints])
            prompt = prompt.replace(
                "[DETERMINATION ROUTING - CRITICAL]", 
                f"{custom_text}\n\n[DETERMINATION ROUTING - CRITICAL]"
            )
        return prompt

    def run(self, user_task: str, initial_data: str = "") -> str:
        """
        Executes a task through the endogenous pruning loop.
        """
        messages = [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": f"Task: {user_task}\nData: {initial_data}"}
        ]
        
        audit_prompt_text = self._build_audit_prompt()
        
        for loop_count in range(self.max_loops):
            # 1. Generate / Correct step
            response = self.client.chat.completions.create(
                model=self.model, 
                messages=messages, 
                temperature=self.generation_temperature
            )
            current_state = response.choices[0].message.content
            messages.append({"role": "assistant", "content": current_state})
            
            # 2. Inject the Metacognitive Audit Prompt
            messages.append({"role": "user", "content": audit_prompt_text})
            
            audit_response = self.client.chat.completions.create(
                model=self.model, 
                messages=messages, 
                temperature=self.audit_temperature
            )
            audit_result = audit_response.choices[0].message.content
            
            if "[STATE: APPROVED]" in audit_result:
                logger.info(f"[EndLoop] Reached optimal state after {loop_count} refinements.")
                # Extract clean payload, removing the routing tag
                clean_payload = audit_result.replace("[STATE: APPROVED]", "").strip()
                return clean_payload
            else:
                # 3. Refine
                messages.pop() # Remove the trigger
                messages.append({"role": "user", "content": f"Correction required: {audit_result}"})
                logger.info(f"🔄 [EndLoop Iteration {loop_count + 1}] Self-correction triggered.")
                
        raise TimeoutError(f"EndLoop System failed to converge to an optimal state within {self.max_loops} loops.")
