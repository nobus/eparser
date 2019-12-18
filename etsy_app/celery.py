# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django.conf import settings
from celery import Celery


app = Celery('etsy_app',
             broker='amqp://guest@localhost//',
             backend='redis://localhost',
             include=['etsy_app.tasks'])

app.conf.broker_transport_options = {'visibility_timeout': 43200}

app.conf.update(
    result_expires=3600,
)

app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'

if __name__ == '__main__':
    app.start()
