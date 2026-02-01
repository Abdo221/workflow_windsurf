# Security Report

## Summary
The News Fetcher application has a minimal attack surface with no user authentication or data storage beyond cached news articles. Main security considerations involve input validation, API key handling, and CORS configuration.

## Threat Model (Lightweight)
- **External API calls**: Backend makes HTTP requests to NewsAPI.org
- **User input**: Category string from frontend
- **Data storage**: SQLite database with news articles
- **Network exposure**: Backend API on localhost:8000, frontend on localhost:5173

## Findings

### High Severity
None found.

### Medium Severity
- **API Key Exposure**: NEWS_API_KEY environment variable required but not enforced
  - Risk: API key could be committed to version control
  - Impact: Potential API abuse or quota exhaustion

### Low Severity
- **CORS Configuration**: Allows all methods/headers from localhost:5173
  - Risk: Overly permissive for local development
  - Impact: Minimal in development context
- **No Rate Limiting**: API endpoint has no rate limiting
  - Risk: Potential abuse if exposed beyond localhost
  - Impact: Resource exhaustion
- **SQLite Database**: No encryption at rest
  - Risk: Cached articles readable if file system compromised
  - Impact: Low; data is public news articles

## Recommendations

### Required (Medium)
1. **API Key Validation**: Add startup check for NEWS_API_KEY
   ```python
   if not os.getenv("NEWS_API_KEY"):
       raise ValueError("NEWS_API_KEY environment variable is required")
   ```

### Optional (Low)
1. **Rate Limiting**: Add basic rate limiting to /news/fetch endpoint
2. **CORS Hardening**: Restrict to specific methods needed (POST, OPTIONS)
3. **Input Sanitization**: Additional validation for category input
4. **Logging**: Add security event logging (failed requests, errors)

## Any Required Follow-ups
- Set NEWS_API_KEY environment variable before running backend
- Consider adding API key validation to prevent accidental deployment without it

## Review Status
**APPROVED** - No high/critical security issues found. Medium severity issue is documented and has clear mitigation.
