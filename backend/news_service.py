import os
import asyncio
import httpx
from datetime import datetime, timedelta
from typing import List, Optional
from models import NewsItem
from database import NewsItemDB, get_session
from sqlmodel import select

class NewsService:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
    
    async def fetch_news(self, category: str, max_attempts: int = 5) -> tuple[List[NewsItem], int]:
        """Fetch news with retry/backoff and fallback to cache."""
        
        # If no API key, return dummy data
        if not self.api_key or self.api_key == "demo_key_for_testing":
            return self._get_dummy_data(category), 1
        
        items = []
        attempts = 0
        
        # Retry with backoff
        for attempt in range(max_attempts):
            attempts += 1
            try:
                async with httpx.AsyncClient() as client:
                    params = {
                        "q": category,
                        "sortBy": "publishedAt",
                        "from": (datetime.utcnow() - timedelta(days=7)).isoformat(),
                        "to": datetime.utcnow().isoformat(),
                        "pageSize": 10,
                        "apiKey": self.api_key
                    }
                    response = await client.get(self.base_url, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Parse items
                    for article in data.get("articles", []):
                        if not article.get("url") or not article.get("publishedAt"):
                            continue
                        item = NewsItem(
                            title=article.get("title", ""),
                            description=article.get("description", ""),
                            url=article["url"],
                            source_name=article.get("source", {}).get("name", ""),
                            published_at=datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
                        )
                        items.append(item)
                    
                    # If we have 10 items, stop
                    if len(items) >= 10:
                        break
                        
            except Exception as e:
                if attempt == max_attempts - 1:
                    # Last attempt failed, will fall back to cache
                    break
                # Wait with exponential backoff
                await asyncio.sleep(0.5 * (2 ** (attempt - 1)))
        
        # Store new items in DB
        await self._store_items(items, category)
        
        # If we have 10 items, return them
        if len(items) >= 10:
            return items[:10], attempts
        
        # Fallback to cache
        cached_items = await self._get_cached_items(category)
        total_items = items + cached_items
        
        # Determine status
        if len(total_items) >= 10:
            return total_items[:10], attempts
        else:
            return total_items, attempts
    
    async def _store_items(self, items: List[NewsItem], category: str):
        """Store items in SQLite, avoiding duplicates by URL."""
        with next(get_session()) as session:
            for item in items:
                # Check if URL already exists
                existing = session.exec(
                    select(NewsItemDB).where(NewsItemDB.url == str(item.url))
                ).first()
                if not existing:
                    db_item = NewsItemDB(
                        title=item.title,
                        description=item.description,
                        url=str(item.url),
                        source_name=item.source_name,
                        published_at=item.published_at,
                        fetched_at=item.fetched_at,
                        category=category
                    )
                    session.add(db_item)
            session.commit()
    
    async def _get_cached_items(self, category: str, limit: int = 10) -> List[NewsItem]:
        """Get cached items for category within last 7 days."""
        with next(get_session()) as session:
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            statement = (
                select(NewsItemDB)
                .where(NewsItemDB.category == category)
                .where(NewsItemDB.published_at >= seven_days_ago)
                .order_by(NewsItemDB.published_at.desc())
                .limit(limit)
            )
            db_items = session.exec(statement).all()
            
            return [
                NewsItem(
                    id=db_item.id,
                    title=db_item.title,
                    description=db_item.description,
                    url=db_item.url,
                    source_name=db_item.source_name,
                    published_at=db_item.published_at,
                    fetched_at=db_item.fetched_at
                )
                for db_item in db_items
            ]
    
    def _get_dummy_data(self, category: str) -> List[NewsItem]:
        """Return dummy news data for demonstration when no API key is available."""
        dummy_articles = {
            "science": [
                {
                    "title": "Scientists Discover New Exoplanet with Potential for Life",
                    "description": "Astronomers have identified a potentially habitable exoplanet located 120 light-years from Earth, showing signs of water vapor in its atmosphere.",
                    "url": "https://example.com/science/exoplanet-discovery",
                    "source_name": "Science Daily",
                    "published_at": datetime.utcnow() - timedelta(days=1)
                },
                {
                    "title": "Breakthrough in Quantum Computing Achieved",
                    "description": "Researchers have successfully demonstrated a quantum computer solving complex problems 1000 times faster than traditional supercomputers.",
                    "url": "https://example.com/science/quantum-breakthrough",
                    "source_name": "Tech Review",
                    "published_at": datetime.utcnow() - timedelta(days=2)
                },
                {
                    "title": "New Vaccine Shows Promise Against Emerging Virus",
                    "description": "Clinical trials indicate high efficacy for a new vaccine developed to combat a recently identified viral strain.",
                    "url": "https://example.com/science/vaccine-breakthrough",
                    "source_name": "Medical Journal",
                    "published_at": datetime.utcnow() - timedelta(days=3)
                }
            ],
            "sports": [
                {
                    "title": "Underdog Team Wins Championship in Stunning Upset",
                    "description": "In a dramatic finale, the underdog team defeated the defending champions with a last-minute score.",
                    "url": "https://example.com/sports/championship-upset",
                    "source_name": "Sports Network",
                    "published_at": datetime.utcnow() - timedelta(hours=6)
                },
                {
                    "title": "Olympic Records Broken in Swimming Finals",
                    "description": "Multiple world records were shattered during the swimming finals at the international competition.",
                    "url": "https://example.com/sports/olympic-records",
                    "source_name": "Athletics Weekly",
                    "published_at": datetime.utcnow() - timedelta(days=1)
                },
                {
                    "title": "Star Player Signs Record-Breaking Contract",
                    "description": "The league's MVP has signed the largest contract in sports history, worth over $500 million.",
                    "url": "https://example.com/sports/record-contract",
                    "source_name": "Sports Business",
                    "published_at": datetime.utcnow() - timedelta(days=2)
                }
            ],
            "technology": [
                {
                    "title": "AI System Achieves Human-Level Performance in Complex Tasks",
                    "description": "A new artificial intelligence system has demonstrated capabilities matching human experts in multiple domains.",
                    "url": "https://example.com/tech/ai-milestone",
                    "source_name": "Tech News",
                    "published_at": datetime.utcnow() - timedelta(hours=12)
                },
                {
                    "title": "Revolutionary Battery Technology Promises Week-Long Phone Life",
                    "description": "Scientists have developed a new battery technology that could extend smartphone battery life to seven days.",
                    "url": "https://example.com/tech/battery-breakthrough",
                    "source_name": "Innovation Hub",
                    "published_at": datetime.utcnow() - timedelta(days=1)
                },
                {
                    "title": "Major Tech Company Announces Quantum Internet Project",
                    "description": "A leading technology company has unveiled plans to build a quantum internet infrastructure for secure communications.",
                    "url": "https://example.com/tech/quantum-internet",
                    "source_name": "Future Tech",
                    "published_at": datetime.utcnow() - timedelta(days=3)
                }
            ]
        }
        
        # Get dummy data for the category, or use general tech news as default
        articles = dummy_articles.get(category.lower(), dummy_articles["technology"])
        
        return [
            NewsItem(
                title=article["title"],
                description=article["description"],
                url=article["url"],
                source_name=article["source_name"],
                published_at=article["published_at"],
                fetched_at=datetime.utcnow()
            )
            for article in articles
        ]
