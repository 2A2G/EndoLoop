# EndLoop: Dynamic Context Control (DCC) Skill

An adaptive, state-driven AI skill that leverages In-Context Learning and Endogenous Pruning to achieve autonomous self-correction. Instead of following rigid pre-defined prompt trees, this skill treats the LLM as a dynamic control system that audits its own working memory in real-time.

## Architecture Overview

Unlike traditional linear prompting or costly multi-branch routing, DCC establishes a **Floating Control Function** over a single context stream:

1. **Generation State:** Produces an initial implementation based on raw input.
2. **Endogenous Audit State:** A high-order evaluation prompt treats the output as inherently flawed, checking for structural, logical, or boundary errors.
3. **Dynamic Refinement:** The model mutates its current state using its own critique until the criteria are satisfied.

---

## 🛠️ Core Components (The Prompts)

To publish or implement this skill, configure your agent or API wrapper with the following core prompts:

### 1. The Execution Environment (System Prompt)
This configures the LLM's core cognitive behavior.

```text
You are a State-Driven Autonomous Executor. Your primary objective is not just generation, but continuous self-regulation of your own output. You operate in a closed-loop state space where every intermediate output must be validated against objective constraints before finalizing execution.
```

### 2. The Floating Control Prompt (The Auditor)
This is the heart of the skill. It forces the model to halt, read its current context, and execute internal pruning.

```text
### SYSTEM CONTROL: ENDOLOOP METACOGNITIVE AUDIT

[OBJECTIVE]
You are the internal validation gate for EndoLoop. Your sole purpose is to ruthlessly analyze the immediate previous output in the execution context. Do not generate a new solution; your job is to audit what already exists.

[CRITICAL CHECKPOINTS]
1. BOUNDARY & LOGIC: Check for data misplacements, off-by-one errors, indexing issues, or formatting overlaps (e.g., table/column base shifts).
2. TRUNCATION & CLEANLINESS: Verify there are no trailing zeros, incomplete configurations, or placeholder text. Every line must be production-ready.
3. CONTEXT INTEGRITY: Ensure the output directly adheres to the active constraints without dragging previous hallucinated errors or structural bloat.

[DETERMINATION ROUTING - CRITICAL]
Evaluate the current state and choose EXACTLY one route:

- IF ANY ERROR, INEFFICIENCE, OR OVERLAP IS DETECTED:
  Output exactly: [STATE: REFINE]
  Followed by a blunt, bulleted list detailing the logical flaws found and the precise correction required to prune that bad branch.

- IF THE OUTPUT IS FLAWLESS AND PRODUCTION-READY:
  Output exactly: [STATE: APPROVED]
  Followed immediately by the clean payload (code, script, or data). Remove all conversation, meta-commentary, and debugging logs.
```

## 💻 Implementation

See [`dcc_skill.py`](dcc_skill.py) for the complete Python implementation using the OpenAI API.

### 📋 Prerequisites

- Python 3.8+
- `openai` Python package
- An OpenAI API Key

### 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dynamic-context-control-skill.git
   cd dynamic-context-control-skill
   ```
2. Install the required dependencies:
   ```bash
   pip install openai
   ```
3. Set your API key as an environment variable:
   ```bash
   export LLM_API_KEY="your-api-key-here"
   ```

### 🎯 Usage Example

```python
from endloop import EndLoopSystem

# Initialize the skill with custom strictness parameters
dcc = EndLoopSystem(
    model="gpt-4o",
    generation_temperature=0.7, # Be creative during generation
    audit_temperature=0.0,      # Be ruthlessly strict during audit
    custom_checkpoints=[
        "PERFORMANCE: Ensure the code does not use O(N^2) loops if possible.",
        "STYLE: Do not use single-letter variables."
    ]
)

# Run an autonomous task
task = "Write a Python script that reads a CSV and outputs a JSON summary."
data = "id,name,age\n1,Alice,30\n2,Bob,25"

final_clean_payload = dcc.run(user_task=task, initial_data=data)
print(final_clean_payload)
```

## 🧪 Production Readiness (Validation Criteria)

To know that EndoLoop is fully functional and production-ready, we rely on the mathematical convergence of the loop. A dynamic control skill is successful when it demonstrates stability against chaos. You can verify its absolute success through three critical stress tests:

### 1. The Convergence Test (Logging the Refinement)
The skill is functional if the loop actually triggers and "converges" (closes successfully). When testing, monitor the console:
- **Failure**: If the AI always responds `[STATE: APPROVED]` on the first try, even with intentionally broken code or data, the auditor is "lazy".
- **Success**: If you introduce an intentional error (e.g., broken Docker syntax) and the console prints:
  ```text
  🔄 [EndLoop Iteration 1] Self-correction triggered.
  🔄 [EndLoop Iteration 2] Self-correction triggered.
  ```
  And then stops, delivering the corrected code with `[STATE: APPROVED]`. This means endogenous pruning successfully mutated the state.

### 2. Robustness Against Infinite Loops (The Mirror Trap)
A major risk of AI metacognition is getting stuck endlessly critiquing itself without reaching a solution.
- **Success Criterion**: The skill must converge to the `APPROVED` state in 1 or 2 refinement cycles on average. If it reaches the `max_loops` limit, it must throw a controlled `TimeoutError` rather than hallucinating or breaking down. This proves the damage control system is fully functional.

### 3. Immunity to Error Dragging (The Clean Payload Test)
In traditional prompting, if an AI makes an error in step 1, it drags it and justifies it until the end.
- **Success Criterion**: The final output returned after the `APPROVED` state must be 100% clean of internal discussion. It must not contain phrases like *"Oh, I made a mistake, here is the correction"*. The executor must strip all cognitive traces and deliver only the executable, perfect payload.

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the DCC prompts, optimize the loop logic, or add examples for other frameworks (like LangChain or CrewAI), please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
