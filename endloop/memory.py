import json

class StateBuffer:
    """
    Live Memory Manager (Context Architecture)
    Handles the State Buffer and Triggered Compression.
    """
    def __init__(self, max_history_messages: int = 6):
        self.goal = ""
        self.confirmed_findings = []
        self.history = []
        self.max_history_messages = max_history_messages

    def set_goal(self, goal: str):
        self.goal = goal

    def add_finding(self, finding: str):
        self.confirmed_findings.append(finding)

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_system_context(self) -> str:
        findings_str = json.dumps(self.confirmed_findings, indent=2)
        return f"GOAL: {self.goal}\nCONFIRMED FINDINGS:\n{findings_str}"

    def needs_compression(self) -> bool:
        # Simple heuristic: if history gets too long, trigger compression
        return len(self.history) > self.max_history_messages

    def compress_history(self, summarizer_func) -> None:
        """
        Triggered Compression (Long-Term Memory).
        Uses a callback to an LLM to summarize the history and extract new findings,
        then wipes the intermediate history.
        """
        if not self.history:
            return

        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.history])
        
        # Summarize using the provided LLM function
        new_findings_raw = summarizer_func(history_text)
        
        # Update state buffer
        self.add_finding(f"Summarized progress: {new_findings_raw}")
        
        # Clear intermediate history, keeping only recent context if necessary
        self.history = []
