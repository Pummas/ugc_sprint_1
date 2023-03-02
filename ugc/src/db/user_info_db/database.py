import logging

import backoff
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from core.config import settings

client = AsyncIOMotorClient(settings.MONGO_URL, serverSelectionTimeoutMS=5000)

db = client[settings.MONGO_DB]


async def get_session() -> AsyncIOMotorClient:
    return db


@backoff.on_exception(
    backoff.expo, ServerSelectionTimeoutError, max_time=60, backoff_log_level=logging.ERROR, raise_on_giveup=True
)
async def check_db_connection():
    logging.info("connecting to MongoDB")
    await db.command("ping")
    return True
