# -*- coding: utf-8 -*-
from rest_framework import serializers

from etsy_app.models import CeleryStat, Listing, Offering, Currency


class CeleryStatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CeleryStat
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False, read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'
