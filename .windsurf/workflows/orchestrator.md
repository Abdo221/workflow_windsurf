---
description: Orchestrates the SDLC workflow from problem description through delivery
---

# Orchestrator Workflow

## Usage
/orchestrator <problem description>

## What it does
- Initializes or overwrites `status.json` with the problem description and sets initial phase/actor.
- Creates `status_history.csv` with the required header and logs the init event.
- Invokes the orchestrator agent to drive the workflow end-to-end.
- The orchestrator agent will:
  - Control phase transitions
  - Maintain `status.json` and append to `status_history.csv`
  - Invoke other agents based on phase/actor state
  - Write `client_report.md` at completion

## Steps
1. Validate that a problem description is provided.
2. Ensure `status.json` and `status_history.csv` exist; create if missing.
3. Write initial `status.json`:
   - `cycle = 0`
   - `problem_description = <provided text>`
   - `current_phase = problem_definition`
   - `current_actor = client`
   - Set timestamps and statuses appropriately
4. Append an `init` row to `status_history.csv`.
5. Invoke the orchestrator agent to continue the workflow.

## Notes
- The orchestrator agent will handle all subsequent agent invocations and phase transitions.
- Review escalation (cycle 0 -> cycle 1) is enforced by the orchestrator agent.
- The workflow ends when the orchestrator writes `client_report.md` and marks the workflow completed.
