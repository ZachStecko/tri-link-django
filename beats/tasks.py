from datetime import datetime
from celery import shared_task
@shared_task
def display_time(x, y):
    print("The time is %s :" % str(datetime.now()))
    return True