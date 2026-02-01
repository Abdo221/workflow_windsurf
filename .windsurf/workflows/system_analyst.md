---
description: Translates problem statement into clear requirements and asks exactly two clarification questions
---

# System Analyst Workflow

## Usage
/system_analyst

## What it does
- Reads the problem description from `status.json`.
- Asks exactly two clarification questions to the client.
- Waits for client answers.
- Creates `requirements.md` with problem summary, requirements, acceptance criteria, and Q&A section.
- Updates `status.json` and logs changes to `status_history.csv`.

## Steps
1. Set `status.json.actor_status = in_progress` and set `timestamps.actor_start_time`.
2. Read `status.json.problem_description`.
3. Ask exactly two clarification questions to the client in chat.
4. Wait for the client to answer both questions.
5. Write `requirements.md` containing:
   - Problem summary
   - Assumptions
   - Functional requirements
   - Non-functional requirements
   - Acceptance criteria
   - Out of scope
   - Clarification Q&A (questions and answers)
6. Set `status.json.actor_status = done` and set `timestamps.actor_end_time`.
7. Append one row to `status_history.csv` for each status change.
8. Notify the orchestrator that `requirements.md` is ready for review.

## Notes
- Only the orchestrator advances phases; this agent only updates its own actor status.
- Do not proceed until both questions are answered.
