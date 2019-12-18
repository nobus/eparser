#!/bin/bash

: '
 sudo rabbitmqctl list_queues
 ...
 workon vsminer
 python manage.py shell

 from vs_app import tasks
 from celery.task.control import inspect

 result = tasks.sleep.delay(120)
 i = inspect()
 i.active()
'

export DJANGO_SETTINGS_MODULE=eparser.settings

celery -A etsy_app worker --loglevel=debug
