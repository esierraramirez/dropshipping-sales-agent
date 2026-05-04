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

    # OpenAI Configuration - Optimizado para bajo costo y baja latencia
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    # Modelos disponibles: gpt-5.4-nano (más económico, recomendado)
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5.4-nano")
    
    # Límites de tokens para optimizar costos
    OPENAI_MAX_INPUT_TOKENS: int = int(os.getenv("OPENAI_MAX_INPUT_TOKENS", "1000"))  # Limita el contexto de entrada
    OPENAI_MAX_OUTPUT_TOKENS: int = int(os.getenv("OPENAI_MAX_OUTPUT_TOKENS", "300"))  # Respuestas concisas
    OPENAI_VERBOSITY: str = os.getenv("OPENAI_VERBOSITY", "medium")  # "medium" es el único soportado en gpt-5.3
    OPENAI_REASONING_EFFORT: str = os.getenv("OPENAI_REASONING_EFFORT", "medium")  # "medium" es el único soportado en gpt-5.3
    
    # WhatsApp Configuration
    WHATSAPP_API_VERSION: str = os.getenv("WHATSAPP_API_VERSION", "v23.0")
    WHATSAPP_APP_ID: str = os.getenv("WHATSAPP_APP_ID", "")
    WHATSAPP_APP_SECRET: str = os.getenv("WHATSAPP_APP_SECRET", "")
    WHATSAPP_SYSTEM_USER_TOKEN: str = os.getenv("WHATSAPP_SYSTEM_USER_TOKEN", "")
    WHATSAPP_BUSINESS_ACCOUNT_ID: str = os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "")
    WHATSAPP_PHONE_NUMBER_ID: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_PHONE_NUMBER: str = os.getenv("WHATSAPP_PHONE_NUMBER", "")

    # CSV audit for CRUD operations
    CRUD_AUDIT_ENABLED: bool = os.getenv("CRUD_AUDIT_ENABLED", "true").lower() == "true"
    CRUD_AUDIT_CSV_PATH: str = os.getenv("CRUD_AUDIT_CSV_PATH", "data/audit/crud_operations.csv")

    # CSV audit for HTTP requests/endpoints
    ENDPOINT_AUDIT_ENABLED: bool = os.getenv("ENDPOINT_AUDIT_ENABLED", "true").lower() == "true"
    ENDPOINT_AUDIT_CSV_PATH: str = os.getenv("ENDPOINT_AUDIT_CSV_PATH", "data/audit/endpoint_requests.csv")


settings = Settings()