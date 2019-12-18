# -*- coding: utf-8 -*-
from django.shortcuts import render

from rest_framework import viewsets

from etsy_app.models import CeleryStat
from etsy_app.serializers import CeleryStatSerializer

class CeleryStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CeleryStat.objects.all()
    serializer_class = CeleryStatSerializer
