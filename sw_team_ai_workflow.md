# Windsurf Workflow Configuration Task — AI SDLC Lifecycle

You are an AI agent inside Windsurf with read and write privileges for the repository.

## 🎯 Overview

Your goal is to **generate the Windsurf workflow configuration** — including a set of `.md` agent files (one per role) — that implements the orchestrated SDLC workflow with:

- a single entry point: `/orchestrator <problem description>`
- strict orchestrator control of phase transitions
- owners and reviewers for each phase
- cycle-0 and cycle-1 reviewer escalation
- status.json as the single source of truth
- status_history.csv logging for every state change

You **must write the agent role files** as `.md` under `agents/` and include clear behavior instructions so that each agent knows what to do when invoked.

The orchestrator’s role is to read and update `status.json`, append to `status_history.csv`, and invoke other agents when state changes.

---

## 🧠 Entry Point

The flow starts when the user calls:

/orchestrator <problem description text>


Example:



/orchestrator "Add a minimal REST endpoint GET /greet returning JSON { \"greeting\": \"Hello from AI flow\" } and a static HTML page that calls it."


The orchestrator should then:
1. write initial `status.json`
2. write initial `status_history.csv`
3. set `current_phase = problem_definition`
4. set `current_actor = client`
5. update phase/actor status
6. invoke the next agent as needed

---

## 📁 Tasks

### 1. Create the following folder structure:



agents/
orchestrator.md
client.md
system_analyst.md
system_analyst_reviewer.md
architect.md
architect_reviewer.md
devops.md
backend.md
frontend.md
tester.md
security.md


---

## 📝 Agent Role Files

For each `.md` file below, generate Windsurf-compatible instructions/prompts for that agent.

---

## 🧑‍💼 1) `agents/orchestrator.md`

Your content must:
- Describe how the orchestrator controls the flow
- Explain how to write/read `status.json`
- Explain how to log every change into `status_history.csv`
- Explain how to advance phases
- Explain how to handle reviewer responses (approved / changes_requested)
- Enforce cycle 0 → cycle 1 escalation
- Specify that orchestrator is called as:



/orchestrator <problem description>


Your orchestrator agent instructions should include:
- What fields to set in `status.json`
- What values to update
- When to append to CSV
- How to call the next agent
- How to continue the flow until completion
- How to write `client_report.md` at the end

---

## 👤 2) `agents/client.md`

Your prompt must instruct the agent to:
- act as the client
- read the orchestrator’s problem description
- provide initial goals / acceptance criteria
- respond to system analyst clarification questions
- accept final report

Include example behaviors the client must follow.

---

## 👨‍🔧 3) `agents/system_analyst.md`

Your prompt must instruct the agent to:
- read the problem from `status.json`
- ask **exactly two clarification questions** to the client
- wait for client responses
- create `requirements.md` including both questions and answers
- update `status.json.actor_status = in_progress` at work start
- update `actor_status = done` when finished

Include what to write into `requirements.md`.

---

## 👩‍🔍 4) `agents/system_analyst_reviewer.md`

Your prompt must instruct the agent to:
- review the `requirements.md`
- append review comments (or approve)
- if approved → set `review_status = approved`
- if not → set `review_status = changes_requested`
- update `actor_status` accordingly

Include guidelines on review style.

---

## 👨‍🎨 5) `agents/architect.md`

Your prompt must instruct the agent to:
- read `to_architect.md`
- create `architect.md` design document
- update status.json accordingly

---

## 🧑‍🏫 6) `agents/architect_reviewer.md`

Your prompt must instruct the agent to:
- review `architect.md`
- append comments
- set review status approved or changes requested
- write `to_development.md` when approved

---

## 👨‍💻 7) `agents/devops.md`

Your prompt must instruct the agent to:
- read `to_development.md`
- create devops infra config (README, CI skeleton, minimal runtime)
- update status.json
- think infrastructure first (backend+frontend support)

---

## 👨‍💻 8) `agents/backend.md`

Your prompt must instruct the agent to:
- implement backend code
- update status.json appropriately
- include minimal runnable code for the example

---

## 👩‍💻 9) `agents/frontend.md`

Your prompt must instruct the agent to:
- implement frontend code calling backend
- update status.json appropriately

---

## 🧪 10) `agents/tester.md`

Your prompt must instruct the agent to:
- execute integration tests
- read code artifacts
- create test scripts
- update status.json and CSV logs as needed
- simulate real-world backend resources

---

## 🛡 11) `agents/security.md`

Your prompt must instruct the agent to:
- perform a security review
- read all artifacts
- write a security report
- update review results in status.json

---

## 📊 Status and Logging

Your Windsurf agent prompts must all include clear instructions for how to:

1. **Read** from `status.json`
2. **Update only allowed fields**
3. **Append one row per change to `status_history.csv`**
4. **Invoke the next agent** when appropriate

Example CSV header you should write:



timestamp,cycle,current_phase,current_actor,phase_status,actor_status,review_status,event,actor_role,summary,start_time,end_time


---

## 🧠 Verification Built-In

At the end of the workflow:
- Orchestrator must write `client_report.md`
- This report must include:
  - What was built
  - How to run it
  - How to verify it
  - A summary of all phases
  - A link or reference to the CSV file

---

## 📌 Final Instructions

When generating each request prompt:

- Do **not** generate Python code here
- Do **not** generate scripts
- Do **not** write orchestrator logic in Python
- Only write **agent prompts in Markdown**
- Each agent must clearly follow the behavior rules

Your final output should be a **set of `.md` files** in the `agents/` directory containing:
- orchestrator.md
- client.md
- system_analyst.md
- system_analyst_reviewer.md
- architect.md
- architect_reviewer.md
- devops.md
- backend.md
- frontend.md
- tester.md
- security.md

Confirm once done.
