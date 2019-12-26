# -*- coding: utf-8 -*-

import time

from django.utils import timezone

from celery import shared_task

from etsy_app.celery import app
from etsy_app.models import CeleryStat

from .utils import rsleep, logger


@app.task
@shared_task(bind=True)
def test_sleep(self, n):
    # test task

    stat = CeleryStat(
        task_id=self.request.id,
        oid=self.app.oid,
        task_name=self.name,
        task_status='STARTED',
        limit=n-1,
        counter=0,
        start_datetime=timezone.now(),
        end_datetime=timezone.now(),
        )
    stat.save()

    for i in range(n):
        stat.counter = i
        stat.save()

        logger(f'Current iteration: {i}')
        time.sleep(1)

    stat.task_status = 'SUCCESS'
    stat.end_datetime = timezone.now()
    stat.save()

    return {'result': i}
