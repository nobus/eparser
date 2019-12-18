# -*- coding: utf-8 -*-
from rest_framework import serializers

from etsy_app.models import CeleryStat


class CeleryStatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CeleryStat
        fields = '__all__'
