from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gateway.api.routes import router
from gateway.core.config import settings
from gateway.core.logger import logger
from gateway.middleware.request_context import RequestContextMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-style gateway for securing LLM requests."
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"], # React/Vite defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestContextMiddleware)
@app.on_event("startup")
async def startup():
    logger.info("LLM Security Gateway started")


app.include_router(router)