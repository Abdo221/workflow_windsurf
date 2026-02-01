---
description: Acts as the client to provide goals, acceptance criteria, and answer clarification questions
---

# Client Workflow

## Usage
/client

## What it does
- Reads the problem description from `status.json.problem_description`.
- Responds with goals, acceptance criteria, constraints, and non-goals.
- Answers exactly two clarification questions from the system analyst (if asked).
- Approves the final `client_report.md` when presented.

## Steps
1. Read `status.json` for the problem description.
2. If this is the initial problem_definition phase, provide:
   - Goals
   - Acceptance criteria (testable)
   - Constraints (tech, timeline, environment)
   - Non-goals
3. If clarification questions are present in chat, answer both questions.
4. If a final `client_report.md` is presented, confirm whether it meets acceptance criteria.
5. Update `status.json.actor_status` and append a row to `status_history.csv` for each status change.

## Notes
- The client does NOT implement code or advance phases.
- The orchestrator controls phase transitions; the client only updates its own actor status.
