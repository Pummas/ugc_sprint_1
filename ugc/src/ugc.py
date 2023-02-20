import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import films_view
from core.config import settings
from core.sentry import init_sentry
from core.tracer import init_tracer
from db import kafka_producer

init_sentry()


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
    init_tracer(app)


@app.on_event("shutdown")
async def shutdown_event():
    logging.debug("app shutdown")
    await kafka_producer.close_kafka()


app.include_router(films_view.router, prefix="/ugc/v1/events", tags=["Events"])
