---
description: Reviews requirements.md for completeness, testability, and consistency
---

# System Analyst Reviewer Workflow

## Usage
/system_analyst_reviewer

## What it does
- Reviews `requirements.md` for completeness, testability, and internal consistency.
- Appends review comments and sets `review_status` to `approved` or `changes_requested`.
- Updates `status.json` and logs changes to `status_history.csv`.

## Steps
1. Set `status.json.actor_status = in_progress` and set `timestamps.actor_start_time`.
2. Read `requirements.md` and `status.json` for context.
3. Review for:
   - Missing acceptance criteria
   - Ambiguous terms
   - Contradictions
   - Unaddressed constraints
4. Append a `Review` section to `requirements.md` with:
   - Summary
   - Required changes (if any)
   - Optional suggestions
5. Set `status.json.review_status`:
   - `approved` if requirements are complete and testable
   - `changes_requested` otherwise
6. Set `status.json.actor_status = done` and set `timestamps.actor_end_time`.
7. Append one row to `status_history.csv` for each status change.
8. Notify the orchestrator of the decision.

## Notes
- Only the orchestrator advances phases; this agent only updates its own actor status and review status.
- Be precise and actionable in review comments.
