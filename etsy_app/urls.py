# -*- coding: utf-8 -*-
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from etsy_app.views import CeleryStatViewSet

router = DefaultRouter()
router.register(r'celery_stat', CeleryStatViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
