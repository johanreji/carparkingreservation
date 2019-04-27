
import django_rq
import redis
from rq.job import Job
from bg import booktimer
from datetime import datetime, timedelta

def ready():
     print("check")
     scheduler = django_rq.get_scheduler('default')

     for job in scheduler.get_jobs():
         job.delete()

     # Have 'mytask' run every 5 minutes
     scheduler.schedule(
     scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
     func=booktimer,                     # Function to be queued
     args=[] ,          # Arguments passed into function when executed
     #kwargs={'foo': 'bar'},         # Keyword arguments passed into function when executed
     interval=60,                   # Time before the function is called again, in seconds
     repeat=10,                     # Repeat this number of times (None means repeat forever)
     #meta={'foo': 'bar'}            # Arbitrary pickleable data on the job itself
)

if __name__ == '__main__':
    ready()

 