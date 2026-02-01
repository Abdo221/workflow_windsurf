# To Architect

## Problem Statement
Build a minimal News Fetcher web app that fetches real news by category and displays up to 10 items with a React frontend and FastAPI backend.

## Acceptance Criteria
- Frontend: Category input, Fetch button, results list, status line (FRESH/CACHED/PARTIAL).
- Backend: POST /news/fetch returns JSON with status, attempts, category, and up to 10 items within last 7 days (UTC), sorted by published_at descending.
- Retry/backoff: up to 5 attempts (0.5s, 1s, 2s, 4s) if fewer than 10 fresh items; fallback to SQLite cache per category.
- Response status logic: FRESH (10 items with at least 1 newly fetched), CACHED (only cached items), PARTIAL (fewer than 10 items).
- Persistence: SQLite with de-duplication by URL; per-category cached queries.
- Validation: category (2–32 chars, allowed chars), URLs valid, published_at parseable.
- E2E test: Playwright/Cypress opens app, types 'science', clicks Fetch, waits for status, asserts 1–10 items with correct fields and dates within 7 days.

## Key Requirements
- Tech stack: React + TypeScript, Python FastAPI, Pydantic v2, SQLite + SQLModel, Playwright or Cypress.
- Must run locally on Windows without paid services.
- Use a commonly available public news API (e.g., NewsAPI.org) for fetching real news.
- SQLite DB created automatically on first run; no seed data; data comes from internet with fallback to cache.

## Constraints
- No auth, pagination, favorites, complex styling, or admin panels.
