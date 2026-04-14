import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "Dropshipping Sales Agent API")
    ENV: str = os.getenv("ENV", "dev")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Negritomotero%24123@db.zywqomqbvxuwbksigcmp.supabase.co:5432/postgres",
    )

    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-this-secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5.3-chat-latest")
    WHATSAPP_API_VERSION: str = os.getenv("WHATSAPP_API_VERSION", "v23.0")


settings = Settings()