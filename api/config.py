# конфиг с использованием ENV
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # подключение к PGSQL с указанными значениями для тестов
    DB_USER: str = "test_user"
    DB_PASSWORD: str = "test_password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "test_db"


    # CORS - разрешенные хосты
    ALLOWED_ORIGINS: str = "http://localhost:3000,https://yourdomain.com"

    # Ключ для JWT токенов используется в  auth.py
    SECRET_KEY: str = "test_secret_key"

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
