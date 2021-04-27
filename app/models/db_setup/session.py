from app.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql://{settings.DATABASE.get('username')}:{settings.DATABASE.get('password')}@{settings.DATABASE.get('database_server')}:{settings.DATABASE.get('port')}/{settings.DATABASE.get('database_name')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModel = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()