# -*- coding: utf-8 -*-

from django.db import models

class CeleryStat(models.Model):
    task_id = models.CharField(primary_key=True, max_length=64)
    task_name = models.CharField(max_length=64)
    task_status = models.CharField(max_length=8, default='PENDING')
    oid = models.CharField(max_length=64)
    limit = models.PositiveIntegerField(default=0)
    counter = models.PositiveIntegerField(default=0)

    start_datetime = models.DateTimeField(auto_now=False)
    end_datetime = models.DateTimeField(auto_now=False)
