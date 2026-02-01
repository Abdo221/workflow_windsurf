# To Development

## Build Targets
- **Backend**: Python FastAPI application with SQLite persistence.
- **Frontend**: React + TypeScript single-page application.
- **Infrastructure**: Local SQLite database; no external services beyond news API.

## Interfaces/Contracts to Implement
### Backend
- POST /news/fetch
  - Request: { "category": "string" }
  - Response: { "status": "FRESH"|"CACHED"|"PARTIAL", "attempts": int, "category": "string", "items": [...] }
- Pydantic models for request/response.
- News fetching service with retry/backoff.
- Cache service for SQLite queries.

### Frontend
- Single component with:
  - Category input (text)
  - Fetch button
  - Results list (render items with title, description, source, published_at, link)
  - Status line (FRESH/CACHED/PARTIAL)
- API client to call POST /news/fetch.

## Required Configs/Env Vars
- Backend: `NEWS_API_KEY` environment variable for the news API.
- Optional: `DATABASE_URL` (default: sqlite:///./news.db).
- Frontend: Backend base URL (default: http://localhost:8000).

## Definition of Done for Development
- Backend starts locally, creates SQLite DB automatically.
- POST /news/fetch returns valid JSON with correct status logic.
- Frontend runs locally, calls backend, renders items and status.
- Retry/backoff and cache fallback work as specified.
- E2E test passes: open app, type 'science', click Fetch, wait for status, assert 1–10 items with correct fields and dates within 7 days.
- README with clear run instructions for backend and frontend.
