---
description: Reviews architect.md and writes to_development.md when approved
---

# Architect Reviewer Workflow

## Usage
/architect_reviewer

## What it does
- Reviews `architect.md` for correctness, feasibility, and alignment with requirements.
- Sets `review_status` to `approved` or `changes_requested`.
- If approved, writes `to_development.md` with build targets and interfaces.
- Updates `status.json` and logs changes to `status_history.csv`.

## Steps
1. Set `status.json.actor_status = in_progress` and set `timestamps.actor_start_time`.
2. Read `architect.md` and `requirements.md`.
3. Review for:
   - Alignment with acceptance criteria
   - Clear responsibilities
   - Feasible run/deploy shape
   - Missing pieces (env vars, configs, interfaces)
4. Append an `Architecture Review` section to `architect.md` with:
   - Summary
   - Required changes (if any)
   - Optional suggestions
5. Set `status.json.review_status`:
   - `approved` if acceptable
   - `changes_requested` otherwise
6. If `approved`, write `to_development.md` containing:
   - Build targets (backend, frontend, infra)
   - Interfaces/contracts to implement
   - Required configs/env vars
   - Definition of done for development
7. Set `status.json.actor_status = done` and set `timestamps.actor_end_time`.
8. Append one row to `status_history.csv` for each status change.
9. Notify the orchestrator of the decision and whether `to_development.md` was produced.

## Notes
- Only the orchestrator advances phases; this agent only updates its own actor status and review status.
- `to_development.md` must be written when approved to enable the development phase.
