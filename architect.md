# Architecture Document

## Overview
Single-page News Fetcher web app with a React TypeScript frontend and Python FastAPI backend. The system fetches real news by category from a public news API, caches results in SQLite, and serves up to 10 items within the last 7 days.

## Architecture Goals
- Minimal, locally runnable on Windows without paid services.
- Clear separation between frontend and backend.
- Robust retry/fallback to ensure responsiveness even when external API fails.
- Simple persistence with caching per category.

## Key Design Decisions
- **Frontend**: React + TypeScript with a single component/page; no routing.
- **Backend**: FastAPI with Pydantic v2 models; SQLite + SQLModel for persistence.
- **External API**: Use a common public news API (e.g., NewsAPI.org) with category support.
- **Caching**: SQLite table `news_items` with unique constraint on `url`; per-category queries.
- **Retry Strategy**: Exponential backoff (0.5s, 1s, 2s, 4s) up to 5 attempts before falling back to cache.
- **Status Logic**: Computed in backend based on fetch results and cache usage.

## System Components and Responsibilities
### Frontend (React + TypeScript)
- Single component: Category input, Fetch button, results list, status line.
- Calls POST /news/fetch with category.
- Renders items with title, description, source, published_at, and link.
- Shows status (FRESH/CACHED/PARTIAL).

### Backend (FastAPI)
- Endpoint: POST /news/fetch.
- Validation: Pydantic models for request/response.
- News fetching service: Calls external news API with retry/backoff.
- Cache service: SQLite queries for cached items per category within 7 days.
- Status computation: Determines FRESH/CACHED/PARTIAL.

### Database (SQLite + SQLModel)
- Tables:
  - `news_items`: id (uuid PK), title, description, url (unique), source_name, published_at, fetched_at, category.
- Indexes: `category`, `published_at`.
- Auto-created on first run.

## Data Flow / Sequence
1. User enters category and clicks Fetch.
2. Frontend POSTs { "category": "<string>" } to /news/fetch.
3. Backend validates category.
4. Backend attempts to fetch from external API up to 5 times with backoff.
5. If 10 items fetched: mark as FRESH, store new items in DB (skip duplicates by URL), return 10 items.
6. If fewer than 10 items after retries: supplement from cache (DB) for same category within 7 days, sorted by published_at desc.
   - If any new items fetched: FRESH; else if only cached items: CACHED.
   - If total items < 10 even after cache: PARTIAL.
7. Backend returns JSON with status, attempts, category, items.
8. Frontend renders items and status line.

## API/Contracts
### POST /news/fetch
**Request:**
```json
{
  "category": "science"
}
```

**Response:**
```json
{
  "status": "FRESH" | "CACHED" | "PARTIAL",
  "attempts": 3,
  "category": "science",
  "items": [
    {
      "id": "uuid",
      "title": "string",
      "description": "string",
      "url": "https://...",
      "source_name": "string",
      "published_at": "2025-01-25T12:00:00Z",
      "fetched_at": "2025-02-01T00:00:00Z"
    }
  ]
}
```

## Error Handling Strategy
- **Invalid category**: 422 with validation error.
- **External API failures**: Retry with backoff; fallback to cache; return CACHED or PARTIAL.
- **Database errors**: 500; log error.
- **Network errors**: Retry; fallback to cache.

## Observability (minimal)
- Backend logs: fetch attempts, cache hits/misses, status determination.
- Frontend: No complex logging; console errors for network issues.

## Security Considerations (high-level)
- Input validation for category.
- URL validation for fetched items.
- No user data storage; minimal attack surface.
- Consider rate limits for external API.

## Testing Strategy
- **Unit tests**: Pydantic model validation, status logic.
- **Integration tests**: Endpoint behavior with mocked external API.
- **E2E tests**: Playwright/Cypress test with real internet calls, as specified in acceptance criteria.

## Implementation Plan (high level)
1. **Backend setup**: FastAPI project, SQLModel models, SQLite setup.
2. **External API integration**: News API client with retry/backoff.
3. **Cache service**: SQLite queries for cached items.
4. **Endpoint implementation**: POST /news/fetch with status logic.
5. **Frontend setup**: React + TypeScript project, single component.
6. **Frontend API call**: Fetch category input, render results and status.
7. **E2E test setup**: Playwright/Cypress configuration and test case.
8. **Local run instructions**: README with steps to start backend and frontend.

## Architecture Review

### Summary
Architecture is sound, feasible, and aligns with requirements. Clear separation of concerns, appropriate tech stack, and realistic retry/fallback strategy.

### Required changes
None.

### Optional suggestions
- Specify environment variable for the news API key (e.g., NEWS_API_KEY).
- Add a note on handling rate limits from the external API.
- Consider adding a health check endpoint for the backend.
