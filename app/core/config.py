# app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Inventory & Asset Management API"
    APP_VERSION: str = "0.5.0"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 100


settings = Settings()