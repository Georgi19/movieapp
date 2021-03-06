from apscheduler.schedulers.background import BlockingScheduler
from main.jobs import update_movies_db,update_people_db,add_cast,add_details_people,add_genres,delete_new
import os
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mysite.settings')
import django
django.setup()
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=2)
def timed_job():
    update_movies_db()


sched.start()
