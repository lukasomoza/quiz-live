from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registra los modelos antes de crear las tablas)
from app.api import quizzes
from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas que no existan. Más adelante lo sustituirás por migraciones (Alembic).
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Quiz Live", lifespan=lifespan)
app.include_router(quizzes.router)


@app.get("/health")
def health():
    return {"status": "ok"}
