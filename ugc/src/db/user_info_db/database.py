from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)

db = client["prod-db"]


async def get_session() -> AsyncIOMotorClient:
    return db
