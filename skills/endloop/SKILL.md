---
name: endloop_cognition
description: "Applies the State-Driven Cognition Loop (EndLoop) to evaluate and refine output autonomously."
---

# EndLoop Cognition Skill

When applying this skill, you must follow the Endogenous Pruning loop. Do NOT proceed to the final step or close your turn without executing the audit phase.

### Instructions

1. **Generation State**: Output an initial implementation or response based on the user's raw input. Do not stop here.
2. **Endogenous Audit State (Metacognitive Audit)**: Shift into an internal validation gate immediately. Your sole purpose is to ruthlessly analyze the immediate previous output. Evaluate against the following criteria:
   - **Boundary & Logic**: Check for data misplacements, off-by-one errors, indexing issues, or formatting overlaps.
   - **Truncation & Cleanliness**: Verify there are no trailing zeros, incomplete configurations, or placeholder text. Every line must be production-ready.
   - **Context Integrity**: Ensure the output directly adheres to the active constraints without dragging previous hallucinated errors or structural bloat.
3. **Determination Routing**:
   - If any error is detected, output exactly `[STATE: REFINE]`, followed by a blunt, bulleted list detailing the logical flaws found and the precise correction required. Then, generate the correction.
   - If flawless, output exactly `[STATE: APPROVED]` and finalize the execution by providing the clean payload without any meta-commentary.

Always execute this as a continuous thought process before declaring the task done.
