# Lab agent instructions

Read ticket.md and docs/feature-map.md first. Restate the acceptance contract before editing.
Change only src/main/java/edu/ai/PriceCalculator.java. Student tests may be added under src/test/java; explanations belong under submissions/.
Do not change the ticket, evaluation/, ci/, workflow, Maven configuration, or Maven wrapper.
Use BigDecimal, keep the public API, and add no dependencies, services, or network calls.
Run ./mvnw -B -ntp test (Windows: .\mvnw.cmd -B -ntp test).
Run python ci/evaluate.py --candidate . --trusted . --out reports for the educational acceptance checks.
Do not invent executed commands or successful results. Say NOT RUN when you cannot run a check.
Keep a short decision and evidence summary. Do not expose private reasoning traces.
Stop after opening the PR and addressing verified findings. A human approves the merge.

Copy-paste task prompts are in docs/prompts-en.md and are written in English. The requested explanatory output may be Greek.
