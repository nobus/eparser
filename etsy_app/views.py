# -*- coding: utf-8 -*-
import numpy as np

from django.views import View
from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from etsy_app.models import CeleryStat, Listing
from etsy_app.serializers import CeleryStatSerializer, PriceSerializer

class CeleryStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CeleryStat.objects.all()
    serializer_class = CeleryStatSerializer

class PriceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Listing.objects.values('listing_id', 'price', 'currency_code', 'url')
    serializer_class = PriceSerializer

    def list(self, request):
        return super().list(request)

class HistogramView(View):
    def get(self, request):
        nbins = int(request.GET.get('nbins', 100))
        minv = int(request.GET.get('minv', -1))
        maxv = int(request.GET.get('maxv', -1))
        currency = request.GET.get('currency', None)

        prices = Listing.objects.values_list('price', flat=True).exclude(price__isnull=True)

        if minv >=0 and maxv >=0:
            prices = prices.filter(price__range=[minv, maxv])

        if currency:
            prices = prices.filter(currency_code=currency)

        h = np.histogram(prices, bins=nbins)

        ret = {
            'bins': h[0].tolist(),
            'edges': h[1].tolist(),
        }

        return JsonResponse(ret)
