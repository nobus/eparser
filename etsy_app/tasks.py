# -*- coding: utf-8 -*-

import time
import requests

from random import randint

from django.utils import timezone
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger

from .celery import app

from etsy_app.models import CeleryStat, Listing


task_logger = get_task_logger(__name__)

def logger(mess, err=False):
    if err:
        task_logger.error(mess)
    else:
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
def get_listings(self, keywords):
    """
    https://www.etsy.com/developers/documentation/reference/listing
    https://www.etsy.com/developers/documentation/getting_started/api_basics#section_pagination
    """

    offset = 0
    url = f'https://openapi.etsy.com/v2/listings/active'
    url_params = {'keywords': keywords, 'api_key': settings.ETSY_API_KEY}

    while True:
        sleep_interval = randint(1, 3)
        logger(f'Fall asleep for {sleep_interval} sec')
        time.sleep(sleep_interval)

        url_params['offset'] = offset
        resp = requests.get(url, params=url_params)

        logger(
            f'X-RateLimit-Limit {resp.headers.get("X-RateLimit-Limit", None)} X-RateLimit-Remaining {resp.headers.get("X-RateLimit-Remaining", None)}')

        if resp.status_code == 200:
            data = resp.json()

            for params in data['results']:
                try:
                    if 'listing_id' in params:
                        if 'price' in params:
                            params['price'] = float(params['price'])

                        if 'is_supply' in params:
                            if params['is_supply'] in ['true', 'True']:
                                params['is_supply'] = True
                            elif params['is_supply'] in ['false', 'False']:
                                params['is_supply'] = False
                            else:
                                params['is_supply'] = None

                        obj, created = Listing.objects.update_or_create(
                            listing_id=params['listing_id'], defaults=params)

                        if obj.keywords and keywords not in obj.keywords:
                            obj.keywords.append(keywords)
                            obj.save()
                        else:
                            obj.keywords = [keywords]
                            obj.save()

                        if created:
                            logger(f'Create new listing {params["listing_id"]}')
                        else:
                            logger(f'Update existing listing {params["listing_id"]}')
                except Exception as e:
                    logger(e, err=True)
                    logger(params, err=True)

            offset = data['pagination']['next_offset']
            logger(f'OFFSET {offset}')

            if offset > 50000:
                logger(f'OFFSET too big {offset}, break!', err=True)
                break

            limit_rem = int(resp.headers.get("X-RateLimit-Remaining", 0))

            if limit_rem <= 0:
                logger(f'Limit remaining {limit_rem}, break!', err=True)
                break
        else:
            logger(f'Status code {resp.status_code}, break!', err=True)
            break

    return {'status': resp.status_code}
