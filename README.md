# Instructor AI review demo

This is the separate instructor demo for the AI software engineering lecture.
The main branch is a correct baseline. demo/review-bug introduces a deliberate,
handwritten rounding regression. demo/review-fixed contains a prepared repair
for fallback. No branch is claimed to be actual AI output.

Read ticket.md for the contract. The acceptance job is ticket-evaluation.
Legacy demo is a separate demonstration check. CodeRabbit is installed through
the GitHub App, not an API key or a workflow. It reviews open PRs automatically.
The instructor passes a valid finding to a free implementation chat and commits
the fix manually. CI reruns; an AI can summarize the final actual evidence.
Merge stays under human control. This is not an autonomous repair/merge agent.
