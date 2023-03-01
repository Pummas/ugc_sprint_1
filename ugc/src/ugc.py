import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from pymongo.errors import ServerSelectionTimeoutError

from api.v1 import bookmarks, films_view, likes, reviews
from core.config import settings
from core.tracer import init_tracer
from db import kafka_producer
from db.user_info_db.database import check_db_connection

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/ugc/openapi",
    openapi_url="/ugc/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup_event():
    logging.debug("app startup")
    kafka_is_connected = await kafka_producer.init_kafka()
    if not kafka_is_connected:
        raise SystemExit("can't connect to kafka brokers")
    try:
        await check_db_connection()
    except ServerSelectionTimeoutError as err:
        logging.error("MongoDB connection error: %s", err)
        raise SystemExit("can't connect to MongoDB")
    init_tracer(app)


@app.on_event("shutdown")
async def shutdown_event():
    logging.debug("app shutdown")
    await kafka_producer.close_kafka()


app.include_router(films_view.router, prefix="/ugc/v1/events", tags=["Events"])
app.include_router(reviews.router, prefix="/ugc/v1/reviews", tags=["Reviews"])
app.include_router(likes.router, prefix="/ugc/v1/likes", tags=["Likes"])
app.include_router(bookmarks.router, prefix="/ugc/v1/bookmarks", tags=["Bookmarks"])
