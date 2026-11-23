from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# Lo que el cliente envía al crear un quiz
class QuizCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None


# Lo que la API devuelve
class QuizOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # permite crear el schema desde el modelo SQLAlchemy

    id: int
    title: str
    description: str | None
    created_at: datetime
