# News Fetcher Python Project

## Project Overview

News Fetcher is a Python-based web application that demonstrates modern software development practices using FastAPI, SQLModel, and integration with external APIs. The project serves as both a functional news aggregation service and a reference implementation for building scalable web applications.

## Architecture

### Backend Stack
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLModel**: ORM for database operations with Pydantic validation
- **SQLite**: Lightweight database for local development
- **Pydantic v2**: Data validation and serialization
- **HTTPX**: Async HTTP client for external API calls
- **Uvicorn**: ASGI server for production deployment

### Key Components

#### 1. API Layer (`main.py`)
- FastAPI application with CORS middleware
- Single endpoint: `POST /news/fetch`
- Request/response validation using Pydantic models
- Error handling and status code management

#### 2. Business Logic (`news_service.py`)
- `NewsService` class encapsulating all news-related operations
- Retry logic with exponential backoff (0.5s, 1s, 2s, 4s)
- Fallback to cached data when external API fails
- Dummy data generation for demo/testing purposes

#### 3. Data Models (`models.py`)
- Pydantic models for request/response validation
- `NewsRequest`: Input validation for category
- `NewsItem`: Individual news article structure
- `NewsResponse`: API response format with status metadata

#### 4. Database Layer (`database.py`)
- SQLModel-based database operations
- Automatic table creation on startup
- Session management and connection handling
- Cache queries for performance optimization

## Features

### Core Functionality
1. **News Fetching**: Retrieves articles from external News API
2. **Caching**: Stores fetched articles in SQLite for performance
3. **Retry Logic**: Handles external API failures gracefully
4. **Status Tracking**: Reports FRESH/CACHED/PARTIAL status
5. **Demo Mode**: Provides dummy data without API key

### Advanced Features
- **Deduplication**: Prevents duplicate articles by URL
- **Category-based Queries**: Supports flexible news categories
- **Date Filtering**: Returns articles from last 7 days
- **Sorting**: Results ordered by publication date
- **Error Resilience**: Graceful degradation on failures

## API Specification

### Endpoint: POST /news/fetch

**Request:**
```json
{
  "category": "science"
}
```

**Response:**
```json
{
  "status": "FRESH|CACHED|PARTIAL",
  "attempts": 3,
  "category": "science",
  "items": [
    {
      "id": "uuid",
      "title": "Article Title",
      "description": "Article description",
      "url": "https://example.com/article",
      "source_name": "Source Name",
      "published_at": "2026-01-30T12:00:00Z",
      "fetched_at": "2026-01-31T12:00:00Z"
    }
  ]
}
```

### Status Logic
- **FRESH**: 10 items returned with at least 1 newly fetched
- **CACHED**: Items returned exclusively from database cache
- **PARTIAL**: Fewer than 10 items even after cache fallback

## Development Setup

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration
```bash
# Set News API key (optional for demo)
export NEWS_API_KEY="your_api_key_here"

# Database URL (optional, defaults to SQLite)
export DATABASE_URL="sqlite:///./news.db"
```

### Running the Application
```bash
# Development server
uvicorn main:app --reload --port 8000

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Testing

### Unit Tests
```bash
# Run backend tests
python -m pytest tests/test_backend.py -v

# Run with coverage
python -m pytest tests/test_backend.py --cov=backend
```

### Integration Tests
```bash
# Run end-to-end tests
cd tests
npx playwright test e2e-integration.spec.ts
```

## Database Schema

### News Items Table
```sql
CREATE TABLE news_items (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT UNIQUE NOT NULL,
    source_name TEXT,
    published_at DATETIME NOT NULL,
    fetched_at DATETIME NOT NULL,
    category TEXT NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_news_items_category ON news_items(category);
CREATE INDEX idx_news_items_published_at ON news_items(published_at);
```

## Error Handling

### External API Failures
- Retry with exponential backoff (max 5 attempts)
- Fallback to cached data
- Return PARTIAL status with available items

### Database Errors
- Automatic table creation on startup
- Connection pooling and session management
- Graceful degradation on database failures

### Validation Errors
- Category length validation (2-32 characters)
- Character validation (letters, digits, space, hyphen)
- URL validation for news articles

## Performance Considerations

### Caching Strategy
- SQLite database for persistent caching
- 7-day retention period for articles
- Category-based indexing for fast queries
- URL-based deduplication

### API Optimization
- Async HTTP requests with HTTPX
- Connection pooling for external API calls
- Batch processing of article data
- Minimal memory footprint

### Scalability
- Stateless API design
- Database connection pooling
- Horizontal scaling capability
- External rate limiting awareness

## Security Considerations

### Input Validation
- Pydantic model validation
- SQL injection prevention via ORM
- URL validation for external links
- Category sanitization

### Data Protection
- No user data storage
- Minimal attack surface
- Secure API key handling
- CORS configuration

### External Dependencies
- Rate limiting awareness
- API key protection
- Timeout handling
- Error information sanitization

## Deployment

### Production Configuration
```bash
# Environment variables
export NEWS_API_KEY="production_key"
export DATABASE_URL="postgresql://user:pass@host/db"

# Run with Gunicorn (alternative to Uvicorn)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker Support
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring and Observability

### Logging
- Structured logging with request tracking
- Error categorization and reporting
- Performance metrics collection
- External API call monitoring

### Health Checks
- Database connectivity verification
- External API availability checks
- Application status endpoint
- Resource usage monitoring

## Future Enhancements

### Planned Features
- Real-time news updates with WebSocket
- Multiple news source aggregation
- User preferences and personalization
- Advanced search and filtering
- News article summarization

### Technical Improvements
- Redis caching for better performance
- PostgreSQL for production deployment
- API rate limiting and throttling
- Comprehensive monitoring dashboard
- Automated testing pipeline

## Contributing

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests
- Document API changes
- Use type hints throughout
- Maintain backward compatibility

### Code Review Process
- Automated testing on PRs
- Code quality checks
- Security review for changes
- Performance impact assessment
- Documentation updates required
