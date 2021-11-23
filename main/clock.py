from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import update_movies_db,update_people_db,add_cast,add_details_people,add_genres,delete_new
from datetime import datetime

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('interval',days=1,next_run_time=datetime.now())
def updt():
    update_movies_db()
    update_people_db()
    add_genres()
    add_details_people()
    add_cast()
    delete_new()
    
scheduler.start()