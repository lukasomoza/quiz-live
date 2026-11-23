from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # De momento SQLite (un archivo local). En la fase de Docker se cambia a PostgreSQL
    # solo tocando esta variable en el .env:
    # DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/quiz
    database_url: str = "sqlite:///./quiz.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
