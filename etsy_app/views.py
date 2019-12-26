# -*- coding: utf-8 -*-
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from etsy_app.models import CeleryStat, Listing, Offering
from etsy_app.serializers import CeleryStatSerializer, PriceSerializer

class CeleryStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CeleryStat.objects.all()
    serializer_class = CeleryStatSerializer

class PriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Listing.objects.values('listing_id', 'price', 'currency_code', 'url')
    serializer_class = PriceSerializer

    def list(self, request):
        return super().list(request)
