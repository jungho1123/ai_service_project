# app/core/config.py
from functools import lru_cache
from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    # .env에서 자동 로드
    DATABASE_URL: str
    API_SERVICE_KEY: str
    FALLBACK_LABEL_PATH: str = ""
    ALLOWED_ORIGINS: list[AnyHttpUrl] | list[str] = ["*"]

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()
