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
    queryset = Listing.objects.values('listing_id', 'price', 'currency__char_code', 'url')
    serializer_class = PriceSerializer

    def list(self, request):
        return super().list(request)

class HistogramView(View):
    def get(self, request):
        nbins = int(request.GET.get('nbins', 100))
        minv = int(request.GET.get('minv', -1))
        maxv = int(request.GET.get('maxv', -1))
        currency = request.GET.get('currency', None)

        fields = ('price', 'currency__nominal', 'currency__value',)
        prices = Listing.objects.select_related().values(*fields)
        prices = prices.exclude(price__isnull=True)

        if minv >=0 and maxv >=0:
            prices = prices.filter(price__range=[minv, maxv])

        if currency:
            prices = prices.filter(currency__char_code=currency)

        h = np.histogram(
            [(obj['currency__value'] / obj['currency__nominal']) * obj['price'] for obj in prices],
            bins=nbins,
            )

        bins = h[0].tolist()
        edges = h[1].tolist()

        ret = {
            'labels': [ [int(edges[c]), int(edges[c+1])] for c, _ in enumerate(bins) ],
            'datasets': [
                {
                    'label': 'Prices',
                    'backgroundColor': '#f87979',
                    'data': bins,
                }
            ]
        }

        return JsonResponse(ret)
