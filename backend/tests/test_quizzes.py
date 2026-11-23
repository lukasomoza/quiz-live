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


def test_get_quiz_not_found():
    r = client.get("/quizzes/999")
    assert r.status_code == 404


def test_get_update_delete_quiz():
    quiz_id = client.post("/quizzes", json={"title": "Viejo"}).json()["id"]

    assert client.get(f"/quizzes/{quiz_id}").json()["title"] == "Viejo"

    r = client.put(f"/quizzes/{quiz_id}", json={"title": "Nuevo", "description": "editado"})
    assert r.status_code == 200
    assert r.json()["title"] == "Nuevo"
    assert r.json()["description"] == "editado"

    assert client.delete(f"/quizzes/{quiz_id}").status_code == 204
    assert client.get(f"/quizzes/{quiz_id}").status_code == 404
    assert client.delete(f"/quizzes/{quiz_id}").status_code == 404


def test_update_not_found():
    r = client.put("/quizzes/999", json={"title": "X"})
    assert r.status_code == 404
