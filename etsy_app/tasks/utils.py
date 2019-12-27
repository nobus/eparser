# -*- coding: utf-8 -*-

import time
import random

from celery.utils.log import get_task_logger


task_logger = get_task_logger(__name__)

def logger(mess, err=False, exc=False):
    if exc:
        task_logger.exception(mess, exc_info=mess)
    elif err:
        task_logger.error(mess)
    else:
        task_logger.info(mess)


def rsleep():
    sleep_interval = random.random()
    logger(f'Fall asleep for {sleep_interval} sec')
    time.sleep(sleep_interval)
