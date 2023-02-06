import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import films_view
from src.core.config import settings
from src.core.tracer import init_tracer
from src.db import kafka_producer

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
    await kafka_producer.init_kafka()
    init_tracer(app)


@app.on_event("shutdown")
async def shutdown_event():
    logging.debug("app shutdown")
    await kafka_producer.close_kafka()


app.include_router(films_view.router, prefix="/ugc/v1/events", tags=["Events"])
