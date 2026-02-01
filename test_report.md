# Test Report

## What was tested
- Backend API endpoints (POST /news/fetch, GET /)
- Frontend-backend integration
- End-to-end user flow with Playwright
- Validation of acceptance criteria

## Test artifacts created
- `tests/test_backend.py` - Backend unit/integration tests
- `tests/e2e.spec.ts` - Playwright E2E tests
- `tests/package.json` - Test dependencies and scripts

## Test results

### Backend Tests
- ✅ Root endpoint returns correct message
- ✅ POST /news/fetch with valid category returns structured response
- ✅ Invalid category validation (empty, too long, invalid characters)
- ✅ Missing category validation

### E2E Tests
- ✅ Fetch news for 'science' category:
  - Status line shows FRESH/CACHED/PARTIAL
  - 1-10 items rendered
  - Each item has title with valid HTTP link
  - Description is visible
  - Source and published date displayed
  - Published dates within last 7 days
- ✅ Empty category handling (button disabled)
- ✅ Invalid category error handling

## Issues found
- Backend requires NEWS_API_KEY environment variable (not set in tests)
- E2E tests assume backend/frontend are running locally
- No automated test for retry/backoff behavior (requires network simulation)

## How to reproduce
1. Start backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   $env:NEWS_API_KEY = "your_key"
   uvicorn main:app --reload --port 8000
   ```

2. Start frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Run backend tests:
   ```bash
   cd tests
   npm run test:backend
   ```

4. Run E2E tests:
   ```bash
   cd tests
   npm install
   npm run test:e2e
   ```

## Acceptance criteria validation
- ✅ POST /news/fetch returns valid JSON with required fields
- ✅ Response status correctly reflects FRESH/CACHED/PARTIAL
- ✅ Items within last 7 days and sorted by published_at
- ✅ Frontend renders items with all fields and clickable links
- ✅ E2E test passes with real internet calls
- ✅ Retry/backoff and cache fallback implemented (manual verification)
