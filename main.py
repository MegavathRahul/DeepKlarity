from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel
from datetime import date

# Create FastAPI instance
app = FastAPI()

# Fake article data (in-memory for now)
articles = [
    {"id": 1, "title": "FastAPI Overview", "content": "Introduction to FastAPI", "category": "Tech", "date": "2024-01-01"},
    {"id": 2, "title": "Python News", "content": "Python 3.10 Features", "category": "Programming", "date": "2024-02-10"},
    {"id": 3, "title": "Web Development", "content": "HTML5 and CSS3 Best Practices", "category": "Web", "date": "2024-03-15"},
]

# Pydantic models
class Article(BaseModel):
    id: int
    title: str
    content: str
    category: str
    date: date

# GET /articles - Retrieve all articles (with optional filtering)
@app.get("/articles", response_model=List[Article])
def get_articles(category: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):
    filtered_articles = articles
    if category:
        filtered_articles = [article for article in filtered_articles if article["category"] == category]
    if start_date:
        filtered_articles = [article for article in filtered_articles if date.fromisoformat(article["date"]) >= start_date]
    if end_date:
        filtered_articles = [article for article in filtered_articles if date.fromisoformat(article["date"]) <= end_date]
    return filtered_articles

# GET /articles/{id} - Retrieve a specific article by ID
@app.get("/articles/{id}", response_model=Article)
def get_article(id: int):
    for article in articles:
        if article["id"] == id:
            return article
    return {"error": "Article not found"}

# GET /search - Search articles by keywords
@app.get("/search", response_model=List[Article])
def search_articles(keyword: str):
    return [article for article in articles if keyword.lower() in article["title"].lower() or keyword.lower() in article["content"].lower()]
