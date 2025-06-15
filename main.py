from fastapi import FastAPI
from api.v1 import bookmarks, likes, reviews
from core.config import settings

app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.include_router(bookmarks.router)
app.include_router(likes.router)
app.include_router(reviews.router)