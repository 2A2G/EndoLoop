import traceback
from typing import Callable

class EndLoopTool:
    """
    Wrapper for EndLoop Tools providing Semantic Filtering and Endogenous Exception Handling.
    """
    def __init__(self, name: str, description: str, func: Callable, max_output_length: int = 1500):
        self.name = name
        self.description = description
        self.func = func
        self.max_output_length = max_output_length

    def execute(self, **kwargs) -> str:
        try:
            result = self.func(**kwargs)
            # Output Sanitization / Semantic Filtering
            result_str = str(result)
            if len(result_str) > self.max_output_length:
                result_str = result_str[:self.max_output_length] + f"\n...[TRUNCATED: Max {self.max_output_length} chars]"
            return result_str
        except Exception as e:
            # Endogenous Exception Handling
            error_trace = traceback.format_exc()
            return f"[Error Observation] Tool '{self.name}' failed: {str(e)}\nTrace: {error_trace}"

def endloop_tool(name: str, description: str, max_output_length: int = 1500):
    """Decorator to easily create EndLoop tools."""
    def decorator(func: Callable):
        return EndLoopTool(name, description, func, max_output_length)
    return decorator
