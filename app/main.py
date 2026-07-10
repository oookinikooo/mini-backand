import os
import sys

for folder in ["src"]:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), folder))

import logging
from contextlib import asynccontextmanager

import web
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import config
from src.db import init_db

logging.basicConfig(level=logging.INFO, format="%(levelname)-10s%(message)s")

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    await init_db()
    yield
    logger.info("...Shutting down")


app = FastAPI(title="SD Backend", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: add frontend host address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in web.all_routers:
    app.include_router(router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=2445, reload=True)
