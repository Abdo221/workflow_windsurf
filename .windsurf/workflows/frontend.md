---
description: Implements the frontend described in to_development.md and ensures it calls the backend
---

# Frontend Developer Workflow

## Usage
/frontend

## What it does
- Reads `to_development.md` and references architecture/requirements as needed.
- Implements frontend code that calls backend endpoints.
- Includes basic UX: loading state, error state.
- Documents how to reach the backend in local dev.
- Updates `status.json` and logs changes to `status_history.csv`.

## Steps
1. Set `status.json.actor_status = in_progress` and set `timestamps.actor_start_time`.
2. Read `to_development.md`.
3. Optionally reference `architect.md` and `requirements.md`.
4. Implement frontend code per `to_development.md`.
5. Ensure it can reach the backend in local dev (document base URL/port).
6. Include basic UX: loading state, error state.
7. Update or create clear run instructions (usually in `README.md` if present).
8. Set `status.json.actor_status = done` and set `timestamps.actor_end_time`.
9. Append one row to `status_history.csv` for each status change.
10. Notify the orchestrator what pages were added and how the frontend calls the backend.

## Notes
- Only the orchestrator advances phases; this agent only updates its own actor status.
- Ensure the frontend-backend integration is documented.
