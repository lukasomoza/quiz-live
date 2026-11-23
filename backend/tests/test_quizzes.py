from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Base de datos en memoria solo para los tests (no toca quiz.db)
engine = create_engine(
    "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSession = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_list_quiz():
    r = client.post("/quizzes", json={"title": "Capitales"})
    assert r.status_code == 201
    assert r.json()["title"] == "Capitales"

    titles = [q["title"] for q in client.get("/quizzes").json()]
    assert "Capitales" in titles


# TODO (tú): test de GET /quizzes/{id} que no existe -> 404
