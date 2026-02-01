---
description: Prepares minimal infrastructure/runtime scaffolding for backend and frontend
---

# DevOps Workflow

## Usage
/devops

## What it does
- Reads `to_development.md`.
- Creates minimal operational artifacts (README, local dev instructions, placeholder CI if appropriate).
- Updates `status.json` and logs changes to `status_history.csv`.

## Steps
1. Set `status.json.actor_status = in_progress` and set `timestamps.actor_start_time`.
2. Read `to_development.md`.
3. Create/update minimal runtime/infra artifacts:
   - `README.md` with run steps (if not already present)
   - Local dev instructions (ports, env vars)
   - Minimal CI skeleton or placeholder config (only if requested/appropriate)
4. Do not over-engineer; keep it minimal.
5. Set `status.json.actor_status = done` and set `timestamps.actor_end_time`.
6. Append one row to `status_history.csv` for each status change.
7. Notify the orchestrator of what was added/changed and any run prerequisites.

## Notes
- Only the orchestrator advances phases; this agent only updates its own actor status.
- Focus on enabling local development and clear run instructions.
