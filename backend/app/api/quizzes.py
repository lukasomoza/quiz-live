from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Quiz
from app.schemas.quiz import QuizCreate, QuizOut

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("", response_model=QuizOut, status_code=201)
def create_quiz(data: QuizCreate, db: Session = Depends(get_db)):
    quiz = Quiz(title=data.title, description=data.description)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz


@router.get("", response_model=list[QuizOut])
def list_quizzes(db: Session = Depends(get_db)):
    return db.scalars(select(Quiz).order_by(Quiz.id)).all()


# TODO (tú):
#   GET    /quizzes/{quiz_id}   -> devuelve uno, o 404 si no existe (mira HTTPException)
#   PUT    /quizzes/{quiz_id}   -> actualiza título/descripción
#   DELETE /quizzes/{quiz_id}   -> borra (status 204)
