from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from celery import Celery
from fastapi.staticfiles import StaticFiles

from .services.database import init_db
from .views import router, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    await init_db()
    yield
    print("Shutting down")


celery = Celery(
    __name__,
    broker=os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379"),
)


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)
app.include_router(tasks.router, prefix="/task")
