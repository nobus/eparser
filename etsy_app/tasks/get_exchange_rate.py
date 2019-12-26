# -*- coding: utf-8 -*-

import requests

from celery import shared_task

from etsy_app.celery import app
from etsy_app.models import Currency, ExchangeRate

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
            num_code = int(values['NumCode'])

            curr_obj, created = Currency.objects.get_or_create(
                num_code=num_code,
                defaults={
                    'num_code': num_code,
                    'num_code_orig': values['NumCode'],
                    'char_code': values['CharCode'],
                    'name': values['Name'],
                })

            if created:
                logger(f'Create new currency {values["CharCode"]}')

            exch_obj = ExchangeRate(
                currency=curr_obj,
                nominal=values['Nominal'],
                value=values['Value'],
            )

            exch_obj.save()
    else:
        logger(f'Status code {resp.status_code}, break!', err=True)
    
    return {'status': resp.status_code}
