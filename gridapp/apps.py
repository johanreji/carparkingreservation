# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig

from bg import geturllen


class GridappConfig(AppConfig):
    name = 'gridapp'
#     def ready(self):
#      scheduler = django_rq.get_scheduler('default')

#      for job in scheduler.get_jobs():
#          job.delete()

#      # Have 'mytask' run every 5 minutes
#      scheduler.schedule(
#      scheduled_time=datetime.utcnow(), # Time for first execution, in UTC timezone
#      func=geturllen,                     # Function to be queued
#      args=["https://github.com/rq/rq-scheduler"],             # Arguments passed into function when executed
#      #kwargs={'foo': 'bar'},         # Keyword arguments passed into function when executed
#      interval=60,                   # Time before the function is called again, in seconds
#      repeat=10,                     # Repeat this number of times (None means repeat forever)
#      #meta={'foo': 'bar'}            # Arbitrary pickleable data on the job itself
# )
