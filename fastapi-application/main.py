from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from api import router as api_router
from core.models import db_helper
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    )
main_app.include_router(
    api_router,
    prefix=settings.api.prefix
)


@main_app.get("/")
async def root():
    return {"message": "Вас приветствует приложение "}


@main_app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True,
                log_level="critical")
