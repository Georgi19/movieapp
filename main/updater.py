from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import updt
from datetime import datetime

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(updt,'interval',days=1,next_run_time=datetime.now())
    
    scheduler.start()