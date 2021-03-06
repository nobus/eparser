# -*- coding: utf-8 -*-
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from etsy_app.views import CeleryStatViewSet, PriceViewSet, HistogramView

router = DefaultRouter()
router.register(r'celery_stat', CeleryStatViewSet)
router.register(r'price', PriceViewSet)


urlpatterns = [
    path('hgram', HistogramView.as_view()),
    path('', include(router.urls)),
]
