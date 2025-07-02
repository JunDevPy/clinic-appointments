# конфиг с использованием ENV
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    # подключение к PGSQL
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    # CORS - разрешенные хосты
    ALLOWED_ORIGINS: str = "http://localhost:3000,https://yourdomain.com"

    # Ключ для JWT токенов используется в  auth.py
    SECRET_KEY: str

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

