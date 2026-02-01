# Requirements Document

## Problem Summary
Build a minimal News Fetcher web app that fetches real news from the internet by category and displays up to 10 items with a simple React frontend and FastAPI backend.

## Assumptions
- A commonly available public news API will be used (e.g., NewsAPI.org) that supports category-based queries and provides required fields.
- The SQLite database will be created automatically on first server run if it does not exist.
- The app runs locally on Windows without external paid services.

## Functional Requirements
- **FR1**: Frontend provides a text input labeled "Category", a "Fetch" button, a results list, and a status line showing FRESH/CACHED/PARTIAL.
- **FR2**: Backend exposes POST /news/fetch accepting { "category": "<string>" }.
- **FR3**: Backend fetches real news from the internet for the given category.
- **FR4**: Backend targets exactly 10 items within the last 7 days (UTC), sorted by published_at descending.
- **FR5**: Backend retries up to 5 attempts with exponential backoff (0.5s, 1s, 2s, 4s) if fewer than 10 valid items are fetched.
- **FR6**: If retries fail to yield 10 items, backend falls back to SQLite cache for that category (items within last 7 days).
- **FR7**: Backend returns JSON with status (FRESH/CACHED/PARTIAL), attempts count, category, and items array.
- **FR8**: Each item includes: id (uuid), title, description, url, source_name, published_at (iso datetime), fetched_at (iso datetime).
- **FR9**: Backend stores every fetched item in SQLite with de-duplication by URL and per-category association.
- **FR10**: Frontend renders up to 10 items showing title, description, source_name, published_at, and a clickable link.
- **FR11**: Status logic:
  - FRESH: 10 items returned and at least 1 newly fetched in this request.
  - CACHED: items returned exclusively from DB because internet fetch failed to produce 10 after retries.
  - PARTIAL: fewer than 10 items returned even after DB fallback.

## Non-Functional Requirements
- **NFR1**: Tech stack: React + TypeScript (frontend), Python FastAPI (backend), Pydantic v2 (validation), SQLite + SQLModel (DB/ORM), Playwright or Cypress (E2E testing).
- **NFR2**: Must run locally on Windows without paid services.
- **NFR3**: Validation rules:
  - category: trimmed, lowercase, length 2..32, allowed characters: letters, digits, space, hyphen.
  - url: valid http(s) URL.
  - published_at: parseable datetime.
- **NFR4**: E2E test: Playwright/Cypress opens app, types 'science', clicks Fetch, waits for status, asserts 1–10 items rendered with correct fields and dates within 7 days.

## Acceptance Criteria (Testable)
- **AC1**: POST /news/fetch with valid category returns JSON with required structure and 10 items (or fewer if partial).
- **AC2**: Response status correctly reflects FRESH/CACHED/PARTIAL per rules.
- **AC3**: Items are within last 7 days UTC and sorted by published_at descending.
- **AC4**: Frontend displays items with all fields and clickable links.
- **AC5**: Retry/backoff behavior is observable when external API is slow or fails.
- **AC6**: Cached items are returned when fresh fetch fails to meet 10-item target.
- **AC7**: E2E test passes end-to-end with real internet calls.

## Out of Scope
- User authentication or accounts.
- Pagination or infinite scroll.
- Saving favorites or history.
- Complex UI/styling beyond functional requirements.
- Admin panels or content management.

## Open Questions
None.

## Clarification Q&A
1. Q: Which external news API(s) should the backend use to fetch real news?
   A: Most commonly and working one (e.g., NewsAPI.org or similar public API).

2. Q: Should the SQLite database file be created automatically on first run, or include explicit setup steps? Should it be initialized with seed data?
   A: No explicit setup steps; DB is created when the server runs if it doesn't exist. Data should come from the internet; if already fetched before, get it from the database.

## Review

### Summary
Requirements are complete, testable, and internally consistent. The document clearly defines functional and non-functional requirements, acceptance criteria, and constraints. The Clarification Q&A resolves open questions.

### Required changes
None.

### Optional suggestions
- Consider specifying a default news API (e.g., NewsAPI.org) and whether an API key is required for local development.
- Add a brief note on error handling for invalid categories or API failures in the acceptance criteria.
