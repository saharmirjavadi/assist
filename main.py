from fastapi import FastAPI
from app.db.session import engine
from app.api.assist import Assistant
from app.db.base_class import Base
from app.models.assist_models import MLModel
from config import Settings

app = FastAPI()
assistant = Assistant()
app.include_router(assistant.router)
Base.metadata.create_all(bind=engine)
