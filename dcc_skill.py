import os
from openai import OpenAI

class DynamicContextControlSkill:
    def __init__(self, model="gpt-4o"):
        self.client = OpenAI(api_key=os.environ.get("LLM_API_KEY"))
        self.model = model
        
    def run(self, user_task, initial_data):
        # Initialize Working Memory
        messages = [
            {"role": "system", "content": "You are a State-Driven Autonomous Executor. Your primary objective is not just generation, but continuous self-regulation of your own output. You operate in a closed-loop state space where every intermediate output must be validated against objective constraints before finalizing execution."},
            {"role": "user", "content": f"Task: {user_task}\nData: {initial_data}"}
        ]
        
        max_loops = 3
        for loop_count in range(max_loops):
            # 1. Generate / Correct step
            response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.2
            )
            current_state = response.choices[0].message.content
            messages.append({"role": "assistant", "content": current_state})
            
            # 2. Inject the Floating Control Prompt to force self-regulation
            audit_prompt = """### FLOATING CONTROL FUNCTION: AUTONOMOUS AUDIT

[CONTEXT EVALUATION TASK]
Analyze the immediate previous output in the chat history. Do not proceed with the next step of the user's task yet. Instead, shift into a Metacognitive Audit State.

[CRITICAL CHECKPOINTS]
1. BOUNDARY LOGIC: Check for off-by-one errors, indexing issues, or data misplacements.
2. LOGICAL CONSISTENCY: Ensure there are no structural contradictions or trailing/redundant values.
3. SYNTAX & CONFIG: Verify that all syntax strictly follows the target environment's rules.

[DETERMINATION ROUTING]
- IF ANY ERROR/INEFFICIENCY IS FOUND: Output "[STATE: REFINE]" followed by a precise critique.
- IF THE OUTPUT IS FLAWLESS: Output "[STATE: APPROVED]" followed immediately by the final clean payload."""
            
            messages.append({
                "role": "user", 
                "content": audit_prompt
            })
            
            audit_response = self.client.chat.completions.create(
                model=self.model, messages=messages, temperature=0.0
            )
            audit_result = audit_response.choices[0].message.content
            
            if "[STATE: APPROVED]" in audit_result:
                # Extract clean payload from audit or return last clean state
                return current_state
            else:
                # Remove the audit prompt trigger to keep context clean, 
                # append the critique, and let the loop run again.
                messages.pop() # Remove the trigger
                messages.append({"role": "user", "content": f"Correction required: {audit_result}"})
                print(f"🔄 [DCC Loop {loop_count + 1}] Self-correction triggered.")
                
        raise TimeoutError("DCC Skill failed to converge to an optimal state within the loop limit.")
