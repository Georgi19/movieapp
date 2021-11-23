from apscheduler.schedulers.background import BackgroundScheduler
from main.jobs import update_movies_db,update_people_db,add_cast,add_details_people,add_genres,delete_new
import os
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mysite.settings')
import django
django.setup()
scheduler = BackgroundScheduler()

@scheduler.scheduled_job('interval',seconds=1,next_run_time=datetime.now())
def updt():
    print ('asdasdas')
    
scheduler.start()