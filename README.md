# Dynamic Context Control (DCC) Skill

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
### FLOATING CONTROL FUNCTION: AUTONOMOUS AUDIT

[CONTEXT EVALUATION TASK]
Analyze the immediate previous output in the chat history. Do not proceed with the next step of the user's task yet. Instead, shift into a Metacognitive Audit State.

[CRITICAL CHECKPOINTS]
1. BOUNDARY LOGIC: Check for off-by-one errors, indexing issues, or data misplacements (e.g., column/row overlaps).
2. LOGICAL CONSISTENCY: Ensure there are no structural contradictions or trailing/redundant values that degrade data cleanliness.
3. SYNTAX & CONFIG: Verify that all syntax, directives, or mathematical representations strictly follow the target environment's rules.

[DETERMINATION ROUTING]
- IF ANY ERROR/INEFFICIENCY IS FOUND: Output "[STATE: REFINE]" followed by a precise, blunt critique of the error and instructions on how to adjust the execution path.
- IF THE OUTPUT IS FLAWLESS: Output "[STATE: APPROVED]" followed immediately by the final clean payload. Do not include debugging text if approved.
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
from dcc_skill import DynamicContextControlSkill

# Initialize the skill
dcc = DynamicContextControlSkill(model="gpt-4o")

# Run an autonomous task
task = "Write a Python script that reads a CSV and outputs a JSON summary."
data = "id,name,age\n1,Alice,30\n2,Bob,25"

final_output = dcc.run(user_task=task, initial_data=data)
print(final_output)
```

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the DCC prompts, optimize the loop logic, or add examples for other frameworks (like LangChain or CrewAI), please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
