# News Fetcher

A minimal web app that fetches news by category with React + TypeScript frontend and Python FastAPI backend.

## 🤖 Windsurf Agent Workflow System

This project demonstrates a complete software development lifecycle orchestrated by specialized AI agents:

### Available Agents (Slash Commands)
- `/orchestrator` - Manages the entire workflow and phase progression
- `/system_analyst` - Translates problems into clear requirements
- `/system_analyst_reviewer` - Reviews requirements for completeness
- `/architect` - Creates technical architecture and design
- `/architect_reviewer` - Reviews architecture for feasibility
- `/devops` - Sets up infrastructure and runtime environment
- `/backend` - Implements Python FastAPI backend
- `/frontend` - Implements React + TypeScript frontend
- `/security` - Performs security reviews
- `/tester` - Validates end-to-end functionality
- `/client` - Provides goals and acceptance criteria

### Workflow Status
- Current phase and agent status tracked in `status.json`
- Complete history logged in `status_history.csv`
- Each agent generates reports and artifacts
- Orchestrator advances phases based on completion criteria

### How to Use the Workflow
1. Start with `/orchestrator` and provide your problem description
2. Follow the agent sequence through requirements → architecture → development → testing
3. Each agent will update status and notify when done
4. Review generated reports at each phase

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- News API key (sign up at https://newsapi.org/) - optional for demo

### Backend
1. Navigate to `backend/`
2. Create a virtual environment:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set environment variable (optional - demo data available without key):
   ```sh
   $env:NEWS_API_KEY = "your_api_key_here"
   ```
5. Run the server:
   ```sh
   uvicorn main:app --reload --port 8000
   ```
   Backend will be available at http://localhost:8000

### Frontend
1. Navigate to `frontend/`
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the dev server:
   ```sh
   npm run dev
   ```
   Frontend will be available at http://localhost:5173

## Usage
1. Open http://localhost:5173
2. Type a category (e.g., "science", "sports", "technology")
3. Click Fetch
4. View results and status (FRESH/CACHED/PARTIAL)

**Demo Mode**: Without an API key, the app returns realistic dummy data for testing.

## API
- POST /news/fetch
  - Request: { "category": "string" }
  - Response: { "status": "FRESH"|"CACHED"|"PARTIAL", "attempts": int, "category": "string", "items": [...] }

## Testing
### Backend Tests
```sh
cd backend
.\venv\Scripts\activate
python -m pytest ../tests/test_backend.py -v
```

### End-to-End Tests
```sh
cd tests
npm install
npx playwright test e2e-integration.spec.ts
```

## Development Notes
- Backend uses SQLite (`news.db`) created automatically on first run
- Retry/backoff: up to 5 attempts (0.5s, 1s, 2s, 4s) before falling back to cache
- Status logic:
  - FRESH: 10 items with at least 1 newly fetched
  - CACHED: items exclusively from DB
  - PARTIAL: fewer than 10 items even after cache fallback
- Dummy data available for demo/testing without API key

## Project Structure
```
├── agents/              # AI agent definitions
├── backend/             # Python FastAPI application
├── frontend/            # React + TypeScript application
├── tests/               # Backend and E2E tests
├── .windsurf/workflows/ # Agent workflow definitions
├── status.json          # Current workflow status
├── status_history.csv   # Complete workflow history
└── *.md                 # Generated reports and documentation
```
