# -*- coding: utf-8 -*-

import requests

from django.conf import settings

from celery import shared_task

from etsy_app.celery import app
from etsy_app.models import Listing, Offering

from .utils import logger, rsleep


def get_offerigngs(listing_obj):
    rsleep()

    url = f'https://openapi.etsy.com/v2/listings/{listing_obj.listing_id}/inventory'
    url_params = {'api_key': settings.ETSY_API_KEY}

    resp = requests.get(url, params=url_params)

    logger(
            f'X-RateLimit-Limit {resp.headers.get("X-RateLimit-Limit", None)} X-RateLimit-Remaining {resp.headers.get("X-RateLimit-Remaining", None)}')

    if resp.status_code == 200:
        data = resp.json()
        products = data['results']['products']

        for product in products:
            for offering in product.get('offerings', []):
                try:
                    params = {
                        'offering_id': offering['offering_id'],
                        'listing': listing_obj,
                        'price_amount': offering['price']['amount'],
                        'price_divisor': offering['price']['divisor'],
                        'original_currency_code': offering['price'].get('original_currency_code', None)
                    }

                    """
                    obj, created = Offering.objects.update_or_create(
                        offering_id=params['offering_id'], defaults=params)

                    if created:
                        logger(f'Create new offering {params["offering_id"]}')
                    else:
                        logger(f'Update existing offering {params["offering_id"]}')
                    """

                    try:
                        obj = Offering.objects.get(offering_id=params['offering_id'])

                        if obj.listing.listing_id != listing_obj.listing_id:
                            logger(f'exist obj.listing_id = {obj.listing.listing_id}, new = {listing_obj.listing_id}', err=True)
                    except Offering.DoesNotExist:
                        obj = Offering(**params)
                        obj.save()

                except Exception as e:
                    logger(e, err=True)
                    logger(params, err=True)

    else:
        logger(f'Status code for inventory {resp.status_code}', err=True)


@app.task
@shared_task(bind=True)
def get_listings(self, keywords):
    """
    https://www.etsy.com/developers/documentation/reference/listing
    https://www.etsy.com/developers/documentation/getting_started/api_basics#section_pagination
    """

    offset = 0
    url = 'https://openapi.etsy.com/v2/listings/active'
    url_params = {'keywords': keywords, 'api_key': settings.ETSY_API_KEY}

    while True:
        rsleep()

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

                        get_offerigngs(obj)
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
