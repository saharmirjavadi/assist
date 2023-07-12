from fastapi import FastAPI
from app.api.assist import Assistant

app = FastAPI()
assistant = Assistant()
app.include_router(assistant.router)
