from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Quiz
from app.schemas.quiz import QuizCreate, QuizOut

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


def get_quiz_or_404(db: Session, quiz_id: int) -> Quiz:
    quiz = db.get(Quiz, quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz no encontrado")
    return quiz


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


@router.get("/{quiz_id}", response_model=QuizOut)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    return get_quiz_or_404(db, quiz_id)


@router.put("/{quiz_id}", response_model=QuizOut)
def update_quiz(quiz_id: int, data: QuizCreate, db: Session = Depends(get_db)):
    quiz = get_quiz_or_404(db, quiz_id)
    quiz.title = data.title
    quiz.description = data.description
    db.commit()
    db.refresh(quiz)
    return quiz


@router.delete("/{quiz_id}", status_code=204)
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = get_quiz_or_404(db, quiz_id)
    db.delete(quiz)
    db.commit()
