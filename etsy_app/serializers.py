# -*- coding: utf-8 -*-
from rest_framework import serializers

from etsy_app.models import CeleryStat, Listing, Offering


class CeleryStatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CeleryStat
        fields = '__all__'


class PriceSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField(read_only=True)
    price = serializers.IntegerField(read_only=True)
    url = serializers.URLField(read_only=True)
    currency_code = serializers.CharField(max_length=3, read_only=True)

    class Meta:
        model = Listing
