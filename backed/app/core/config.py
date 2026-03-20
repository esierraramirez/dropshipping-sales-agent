import os
from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = "Dropshipping Sales Agent API"
    ENV: str = os.getenv("ENV", "dev")

    # Usar SQLite por defecto en desarrollo, PostgreSQL solo si se especifica
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./catalog.db" if os.getenv("ENV", "dev") == "dev" else "postgresql+psycopg2://app:app@localhost:5432/dropshipping"
    )

    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")


settings = Settings()