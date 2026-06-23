# EndLoop Architecture Design

## 1. The Metacognitive Engine (Base System Prompt)
This is the "operating personality" of the Skill. It injects the rules of Self-Regulation and Endogenous Pruning through explicit instructions.
- **Role Definition**: The AI is instructed to act as a state engine, not a conversational assistant.
- **Strict ReAct Format Obligation**: The Skill is required to respond by strictly structuring its output in three phases: `[Internal Thought]`, `[Action/Tool]`, and `[Awaiting Observation]`.
- **Pruning Mechanism**: An explicit heuristic rule is included: *"Before invoking a tool, you must list two possible approaches in your Internal Thought and explicitly write why you discard one of them based on the current context."*

## 2. The Live Memory Manager (Context Architecture)
The Skill cannot rely on an infinite chat history.
- **State Buffer (Short-Term Memory)**: A block of text at the beginning of each iteration containing the original goal and a JSON/list of confirmed findings so far.
- **Triggered Compression (Long-Term Memory)**: A script that monitors token consumption. When interactions reach a critical threshold, the Skill triggers a subroutine that reads the history, extracts the resolution, updates the State Buffer, and clears intermediate messages.

## 3. The Tool Interface (State-Based Execution)
The principles of dynamic control require the Skill to interact with the outside world without breaking or overflowing.
- **Deterministic Tools**: The functions the Skill has access to do not return raw data.
- **Output Sanitization**: If the Skill asks to read a document, the tool returns a summary or paginated data.
- **Endogenous Exception Handling**: If a tool fails, the error is not shown to the user. The Skill's system catches the error and silently returns it to the model as an `[Error Observation]`, forcing it to apply State-Based Execution to try another path.

## Technical Implementation Synthesis

| Theoretical Principle | Component in the Skill | Practical Function |
| :--- | :--- | :--- |
| **Cognitive Self-Regulation** | Strict ReAct Loop | Forces the model to justify its intent before executing any external action. |
| **Pruning Heuristic** | Self-Critique Prompt | Forces the AI to internally evaluate if its plan makes sense before spending compute. |
| **State-Based Execution** | Callback Handling | Tools return control to the model instead of crashing the flow on unexpected errors. |
| **Metacognitive Compression** | Summarization Trigger | Transforms 2000 tokens of error logs into 150 tokens of "diagnosed root cause". |
| **Semantic Filtering** | Sanitized Interface | Limits API responses to paginated or truncated formats (e.g., max 50 lines). |
