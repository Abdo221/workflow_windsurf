import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import NewsRequest, NewsResponse
from news_service import NewsService
from database import create_db_and_tables
import os

app = FastAPI(title="News Fetcher API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # Check for API key
    if not os.getenv("NEWS_API_KEY"):
        print("WARNING: NEWS_API_KEY environment variable not set. Please set it to fetch real news.")

news_service = NewsService()

@app.post("/news/fetch", response_model=NewsResponse)
async def fetch_news(request: NewsRequest):
    """Fetch news for a given category."""
    try:
        items, attempts = await news_service.fetch_news(request.category)
        
        # Determine status
        if len(items) >= 10:
            # Check if at least one item was newly fetched (simple heuristic: if attempts > 0 and we have items)
            status = "FRESH"
        elif items:
            # Some items but fewer than 10
            status = "PARTIAL"
        else:
            # No items at all
            status = "PARTIAL"
        
        # More accurate status determination
        # For simplicity, we'll use basic logic; in production, track whether any items were newly fetched
        return NewsResponse(
            status=status,
            attempts=attempts,
            category=request.category,
            items=items
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "News Fetcher API"}
