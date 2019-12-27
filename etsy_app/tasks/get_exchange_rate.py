# -*- coding: utf-8 -*-

import requests

from celery import shared_task

from etsy_app.celery import app
from etsy_app.models import Currency

from .utils import logger


@app.task
@shared_task(bind=True)
def get_exchange_rate(self):
    """
    https://www.cbr-xml-daily.ru/daily_json.js
    """

    resp = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')

    if resp.status_code == 200:
        data = resp.json()

        for values in data['Valute'].values():
            curr_obj, created = Currency.objects.update_or_create(
                char_code=values['CharCode'],
                defaults={
                    'char_code': values['CharCode'],
                    'name': values['Name'],
                    'previous': values['Previous'],
                    'nominal': values['Nominal'],
                    'value': values['Value'],
                })

            if created:
                logger(f'Create new currency {values["CharCode"]}')
            else:
                logger(f'Update currency {values["CharCode"]}')
    else:
        logger(f'Status code {resp.status_code}, break!', err=True)
    
    return {'status': resp.status_code}
