from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config

engine = create_engine(config('DB_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
