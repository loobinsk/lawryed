import os
from celery import Celery, shared_task

from celery.schedules import crontab
import logging
# import django.conf

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("lawyerd")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# @app.add_periodic_task(schedule=60)


# app.conf.ONCE = {
#   'backend': 'celery_once.backends.Redis',
#   'settings': {
#     'url': 'redis://localhost:6379/0',
#     'default_timeout': 60 * 60,
#     'blocking': True,
#     'blocking_timeout': 30
#   }
# }


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender: Celery, **kwargs):
#     # sender.add_periodic_task(60.0, compliant_work.s(), name='compliant work')
#
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#
#
# #
# #     # Calls test('world') every 30 seconds
# #     sender.add_periodic_task(30.0, test.s('world'), expires=10)
# #
# #     # Executes every Monday morning at 7:30 a.m.
# #     sender.add_periodic_task(
# #         crontab(hour=7, minute=30, day_of_week=1),
# #         test.s('Happy Mondays!'),
# #     )
# #
# #
# @app.task
# def test(arg):
#     print(arg)

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     pass
#     sender.add_periodic_task(10, debug_task.s(), name='scan for expired accounts every 4 hours')
#
#
# @app.task(bind=True)
# # @app.task
# def debug_task(self):
#     with open('celery_beat_test.txt', 'wt') as f:
#         f.write(self.request)
#     e = 3/0
#     print(e)
#     # logging.info('Request: {0!r}'.format(self.request))
#
