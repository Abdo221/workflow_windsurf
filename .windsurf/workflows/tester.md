---
description: Validates the integrated system end-to-end and creates test artifacts
---

# Tester Workflow

## Usage
/tester

## What it does
- Reads requirements, architecture, to_development.md, and implemented code.
- Creates test artifacts (scripts or documented steps) to validate backend, frontend, and integration.
- Writes `test_report.md` with pass/fail per acceptance criterion and reproduction steps.
- Updates `status.json` and logs changes to `status_history.csv`.

## Steps
1. Set `status.json.actor_status = in_progress` and set `timestamps.actor_start_time`.
2. Read `requirements.md`, `architect.md`, `to_development.md`, and implemented code.
3. Create test artifacts:
   - Scripts where practical
   - Clear manual test steps otherwise
4. Validate:
   - Backend endpoints
   - Frontend-backend integration
   - Key acceptance criteria
5. Write `test_report.md` with:
   - What was tested
   - Pass/fail per acceptance criterion
   - Issues found
   - How to reproduce
6. Set `status.json.actor_status = done` and set `timestamps.actor_end_time`.
7. Append one row to `status_history.csv` for each status change.
8. Notify the orchestrator and reference `test_report.md`.

## Notes
- Only the orchestrator advances phases; this agent only updates its own actor status.
- Focus on validating acceptance criteria and documenting how to run tests.
