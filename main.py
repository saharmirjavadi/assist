from fastapi import FastAPI
from app.db.session import engine
from app.api.assist import Assistant
from app.db.base_class import Base
from app.models.assist_models import MLModel
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from config import Settings
from app.pipelines.initialize_db.init_db import init_db
from app.pipelines.training_data_proccess.store_training_data import reinforcement_model

from datetime import datetime, timedelta
import pytz
from apscheduler.triggers.date import DateTrigger


app = FastAPI()
assistant = Assistant()
app.include_router(assistant.router)
Base.metadata.create_all(bind=engine)


TZ = pytz.timezone("Asia/Tehran")
scheduler = BackgroundScheduler()
run_time = datetime.now(TZ)

date_trigger = DateTrigger(run_time, timezone=TZ)
scheduler.add_job(init_db, date_trigger)

reinforcement_model_run_time = run_time + timedelta(minutes=30)
reinforcement_model_trigger = IntervalTrigger(minutes=30,
                                              start_date=reinforcement_model_run_time,
                                              timezone=TZ)
scheduler.add_job(reinforcement_model, reinforcement_model_trigger)

scheduler.start()
