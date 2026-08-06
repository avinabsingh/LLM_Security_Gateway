from fastapi import FastAPI

from gateway.api.routes import router
from gateway.core.config import settings
from gateway.core.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-style gateway for securing LLM requests."
)


@app.on_event("startup")
async def startup():
    logger.info("LLM Security Gateway started")


app.include_router(router)