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

    class Config:
        case_sensitive = True

settings = Settings()
