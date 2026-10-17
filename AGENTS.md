# Lab agent instructions

Understand ticket.md and docs/feature-map.md, inspect the repository, and restate the objective before implementing.
Choose the implementation, file layout, refactorings, supporting tests, build changes, and tools needed to meet the objective.
Explore and change any project files needed to meet the objective.
Preserve the agreed public behavior and API. Explain how your changes serve the objective.
Use the evaluation tools to test your solution and investigate failures. The independent acceptance run evaluates the complete candidate project against the agreed contract.
Run ./mvnw -B -ntp test (Windows: .\mvnw.cmd -B -ntp test).
Run python ci/evaluate.py --candidate . --trusted . --out reports for the educational acceptance checks.
Do not invent executed commands or successful results. Say NOT RUN when you cannot run a check.
Keep a short decision and evidence summary. Do not expose private reasoning traces.
Prepare the PR and address verified findings. The final merge decision uses the evidence and the team's approval process.

Copy-paste task prompts are in docs/prompts-en.md and are written in English. The requested explanatory output may be Greek.
