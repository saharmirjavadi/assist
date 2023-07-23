from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Settings

settings = Settings()

engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
