from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # TODO (tú): cuando exista User, añade owner_id = ForeignKey("users.id")
    # TODO (tú): relación con las preguntas:
    #   questions: Mapped[list["Question"]] = relationship(back_populates="quiz", cascade="all, delete-orphan")


# TODO (tú): modelo Question  -> tabla "questions"
#   id, quiz_id (ForeignKey a quizzes.id), position, text, time_limit_s
#
# TODO (tú): modelo Option    -> tabla "options"
#   id, question_id (ForeignKey a questions.id), text, is_correct
#
# Pista: mira "relationship" y "ForeignKey" en la doc de SQLAlchemy 2.0 (ORM Quick Start).
