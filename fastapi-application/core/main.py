import uvicorn
from fastapi import FastAPI
from loguru import logger

from api import router as api_router
from core.config import settings

app = FastAPI()
app.include_router(
    api_router,
    prefix=settings.api.prefix
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run(app="main:app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True,
                log_level="critical")
