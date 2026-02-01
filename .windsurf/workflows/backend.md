---
description: Implements the backend described in to_development.md
---

# Backend Developer Workflow

## Usage
/backend

## What it does
- Reads `to_development.md` and references architecture/requirements as needed.
- Implements backend code matching the specified API/contract.
- Ensures the backend starts locally and exposes required endpoints.
- Updates `status.json` and logs changes to `status_history.csv`.

## Steps
1. Set `status.json.actor_status = in_progress` and set `timestamps.actor_start_time`.
2. Read `to_development.md`.
3. Optionally reference `architect.md` and `requirements.md`.
4. Implement backend code per `to_development.md`.
5. Ensure the backend starts locally and exposes required endpoints.
6. Update or create clear run instructions (usually in `README.md` if present).
7. Set `status.json.actor_status = done` and set `timestamps.actor_end_time`.
8. Append one row to `status_history.csv` for each status change.
9. Notify the orchestrator what endpoints were implemented and how to run the backend.

## Notes
- Only the orchestrator advances phases; this agent only updates its own actor status.
- Keep the solution minimal, runnable, and aligned with acceptance criteria.
