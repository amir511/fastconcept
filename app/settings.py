from pydantic import BaseSettings
from typing import Dict, Any

class Settings(BaseSettings):
    DEBUG: bool = True
    DATABASE: Dict[str, Any] = {
        'database_name':'fastconceptdb',
        'username':'fastconceptuser',
        'password':'fastconcept',
        'port':5432,
        'database_server': 'localhost',
    }
    SECRET_KEY: str = 'kn+qZbFvY4pJvKtKaVbJlVBozf0AdPT5jfSa2t0pFY1R8N1QCer3kQ=='
    JWT_ACCESS_TOKEN_EXPIRATION: int = 60
    JWT_REFRESH_TOKEN_EXPIRATION: int = 1440
    class Config:
        case_sensitive = True

settings = Settings()
