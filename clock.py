from apscheduler.schedulers.background import BackgroundScheduler
from main.jobs import update_movies_db,update_people_db,add_cast,add_details_people,add_genres,delete_new
import os
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mysite.settings')
import django
django.setup()
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=5)
def timed_job():
    print('This job is run every three minutes.')


sched.start()
