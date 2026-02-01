from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
from datetime import datetime
import uuid

class NewsItemDB(SQLModel, table=True):
    __tablename__ = "news_items"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    description: str
    url: str = Field(unique=True, index=True)
    source_name: str
    published_at: datetime
    fetched_at: datetime
    category: str = Field(index=True)

# Database setup
DATABASE_URL = "sqlite:///./news.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    with Session(engine) as session:
        yield session
