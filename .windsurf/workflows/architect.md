---
description: Creates architecture/design document based on approved requirements
---

# Architect Workflow

## Usage
/architect

## What it does
- Reads `to_architect.md` (prepared by orchestrator from approved requirements).
- Creates `architect.md` with design decisions, components, data flow, and implementation plan.
- Updates `status.json` and logs changes to `status_history.csv`.

## Steps
1. Set `status.json.actor_status = in_progress` and set `timestamps.actor_start_time`.
2. Read `to_architect.md`.
3. Optionally reference `requirements.md` for details.
4. Write `architect.md` containing:
   - Overview
   - Architecture goals
   - Key design decisions
   - System components and responsibilities
   - Data flow / sequence description
   - API/contracts (as applicable)
   - Error handling strategy
   - Observability approach (minimal)
   - Security considerations (high-level)
   - Testing strategy
   - Implementation plan (high level)
5. Set `status.json.actor_status = done` and set `timestamps.actor_end_time`.
6. Append one row to `status_history.csv` for each status change.
7. Notify the orchestrator that `architect.md` is ready for review.

## Notes
- Only the orchestrator advances phases; this agent only updates its own actor status.
- Ensure the design meets acceptance criteria from requirements.
