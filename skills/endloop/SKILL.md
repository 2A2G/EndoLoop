---
name: endloop_cognition
description: "Applies the State-Driven Cognition Loop (EndLoop) to evaluate and refine output autonomously."
---

# EndLoop Cognition Skill

When applying this skill, you must follow the Endogenous Pruning loop. Do NOT proceed to the final step or close your turn without executing the audit phase.

### Instructions

1. **Generation State**: Output an initial implementation or response based on the user's raw input. Do not stop here.
2. **Endogenous Audit State**: Shift into a Metacognitive Audit State immediately. Evaluate your output against the following criteria:
   - **Boundary Logic**: Are there off-by-one errors or structural misalignments?
   - **Logical Consistency**: Are there contradictions or redundant values?
   - **Syntax & Rules**: Does it strictly follow the target environment's rules?
3. **Determination Routing**:
   - If any flaw is found, output `[STATE: REFINE]` with a precise critique, then immediately generate a new version.
   - If flawless, output `[STATE: APPROVED]` and finalize the execution.

Always execute this as a continuous thought process before declaring the task done.
