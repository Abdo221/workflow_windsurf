---
description: Performs a security review of all artifacts and code
---

# Security Reviewer Workflow

## Usage
/security

## What it does
- Reviews all artifacts and code for common security issues.
- Writes `security_report.md` with findings and recommendations.
- Sets `review_status` to `approved` or `changes_requested`.
- Updates `status.json` and logs changes to `status_history.csv`.

## Steps
1. Set `status.json.actor_status = in_progress` and set `timestamps.actor_start_time`.
2. Read all artifacts:
   - `requirements.md`
   - `architect.md`
   - `to_development.md`
   - Codebase changes
   - `test_report.md` (if present)
3. Review for:
   - Input validation
   - Injection risks
   - Secrets handling
   - Insecure defaults (CORS, debug mode)
   - Dependency risk (as applicable)
4. Write `security_report.md` with:
   - Summary
   - Threat model (lightweight)
   - Findings (severity-tagged)
   - Recommendations
   - Any required follow-ups
5. Set `status.json.review_status`:
   - `approved` if no high/critical issues block release
   - `changes_requested` if fixes are required before delivery
6. Set `status.json.actor_status = done` and set `timestamps.actor_end_time`.
7. Append one row to `status_history.csv` for each status change.
8. Notify the orchestrator and reference `security_report.md`.

## Notes
- Only the orchestrator advances phases; this agent only updates its own actor status and review status.
- Be clear about required fixes vs optional suggestions.
