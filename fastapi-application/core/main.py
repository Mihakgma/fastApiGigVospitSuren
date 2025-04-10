import uvicorn
from fastapi import FastAPI
from loguru import logger

from api import router as api_router

app = FastAPI()
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run("main:app", port=8000, reload=True, log_level="critical")
