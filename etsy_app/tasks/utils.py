# -*- coding: utf-8 -*-

import time

from random import randint

from celery.utils.log import get_task_logger


task_logger = get_task_logger(__name__)

def logger(mess, err=False):
    if err:
        task_logger.error(mess)
    else:
        task_logger.info(mess)


def rsleep():
    sleep_interval = randint(1, 3)
    logger(f'Fall asleep for {sleep_interval} sec')
    time.sleep(sleep_interval)
