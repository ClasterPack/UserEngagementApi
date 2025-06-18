from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings

client = AsyncIOMotorClient(settings.mongo_url)
mongo_db = client.bookmark_app
