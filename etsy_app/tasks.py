# -*- coding: utf-8 -*-

import time
import requests

from django.utils import timezone
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger

from .celery import app

from etsy_app.models import CeleryStat, Listing


task_logger = get_task_logger(__name__)

def logger(mess):
    task_logger.info(mess)

@app.task
@shared_task(bind=True)
def sleep(self, n):
    # test task

    stat = CeleryStat(
        task_id=self.request.id,
        oid=self.app.oid,
        task_name=self.name,
        task_status='STARTED',
        limit=n-1,
        counter=0,
        start_datetime=timezone.now(),
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


@app.task
@shared_task(bind=True)
def get_listings(self):
    """
    https://www.etsy.com/developers/documentation/reference/listing
    """

    url_params = {'keywords': 'weaving', 'api_key': settings.ETSY_API_KEY}
    url = f'https://openapi.etsy.com/v2/listings/active'

    resp = requests.get(url, params=url_params)

    data = resp.json()

    for params in data['results']:
        print(params)

        if 'price' in params:
            params['price'] = float(params['price'])


        if 'is_supply' in params:
            if params['is_supply'] in ['true', 'True']:
                params['is_supply'] = True
            elif params['is_supply'] in ['false', 'False']:
                params['is_supply'] = False
            else:
                params['is_supply'] = None

        obj = Listing(**params)
        obj.save()

    return {'status': resp.status_code}
