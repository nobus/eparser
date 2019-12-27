# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.postgres.fields import ArrayField

class CeleryStat(models.Model):
    task_id = models.CharField(primary_key=True, max_length=64)
    task_name = models.CharField(max_length=64)
    task_status = models.CharField(max_length=8, default='PENDING')
    oid = models.CharField(max_length=64)
    limit = models.PositiveIntegerField(default=0)
    counter = models.PositiveIntegerField(default=0)

    start_datetime = models.DateTimeField(auto_now=False)
    end_datetime = models.DateTimeField(auto_now=False)

class Currency(models.Model):
    """
    https://www.cbr-xml-daily.ru/daily_json.js
    """
    char_code = models.CharField(max_length=3, primary_key=True)
    name = models.TextField()
    nominal = models.PositiveSmallIntegerField(default=1)
    value = models.PositiveIntegerField()
    previous = models.PositiveIntegerField()


class Listing(models.Model):
    """
    https://www.etsy.com/developers/documentation/reference/listing#section_fields
    """

    listing_id = models.BigIntegerField(primary_key=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    state = models.CharField(max_length=16, null=True, blank=True, default=None)
    user_id = models.BigIntegerField(null=True, blank=True, default=None)
    category_id = models.BigIntegerField(null=True, blank=True, default=None)
    title = models.TextField(null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    creation_tsz = models.FloatField(null=True, blank=True, default=None)
    ending_tsz = models.FloatField(null=True, blank=True, default=None)
    original_creation_tsz = models.FloatField(null=True, blank=True, default=None)
    last_modified_tsz = models.FloatField(null=True, blank=True, default=None)
    price = models.FloatField(null=True, blank=True, default=None)
    quantity = models.PositiveIntegerField(null=True, blank=True, default=None)
    sku = ArrayField(models.CharField(max_length=2), blank=True, null=True)
    tags = ArrayField(models.TextField(), blank=True, null=True)
    category_path = ArrayField(models.TextField(), blank=True, null=True)
    category_path_ids = ArrayField(models.PositiveIntegerField(), blank=True, null=True)
    materials = ArrayField(models.TextField(), blank=True, null=True)
    shop_section_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    featured_rank = models.IntegerField(null=True, blank=True, default=None)
    state_tsz = models.PositiveIntegerField(null=True, blank=True, default=None)
    url = models.URLField(max_length=256, null=True, blank=True, default=None)
    views = models.PositiveIntegerField(null=True, blank=True, default=None)
    num_favorers = models.PositiveIntegerField(null=True, blank=True, default=None)
    shipping_template_id = models.BigIntegerField(null=True, blank=True, default=None)
    processing_min = models.PositiveIntegerField(null=True, blank=True, default=None)
    processing_max = models.PositiveIntegerField(null=True, blank=True, default=None)
    who_made = models.CharField(max_length=16, null=True, blank=True, default=None)
    is_supply = models.NullBooleanField()
    when_made = models.CharField(max_length=16, null=True, blank=True, default=None)
    item_weight = models.FloatField(null=True, blank=True, default=None)
    item_weight_unit = models.CharField(max_length=2, null=True, blank=True, default=None)
    item_length = models.FloatField(null=True, blank=True, default=None)
    item_width = models.FloatField(null=True, blank=True, default=None)
    item_height = models.FloatField(null=True, blank=True, default=None)
    item_dimensions_unit = models.CharField(max_length=2, null=True, blank=True, default=None)
    is_private = models.NullBooleanField()
    recipient = models.CharField(max_length=16, null=True, blank=True, default=None)
    occasion = models.TextField(null=True, blank=True, default=None)
    style = ArrayField(models.TextField(), blank=True, null=True)
    non_taxable = models.NullBooleanField()
    is_customizable = models.NullBooleanField()
    is_digital = models.NullBooleanField()
    file_data = models.TextField(null=True, blank=True, default=None)
    should_auto_renew = models.NullBooleanField()
    language = models.CharField(max_length=16, null=True, blank=True, default=None)
    has_variations = models.NullBooleanField()
    taxonomy_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    taxonomy_path = ArrayField(models.TextField(), blank=True, null=True)
    suggested_taxonomy_id = models.PositiveIntegerField(null=True, blank=True, default=None)
    used_manufacturer = models.NullBooleanField()
    is_vintage = models.NullBooleanField()

    keywords = ArrayField(models.TextField(), blank=True, null=True)


class Offering(models.Model):
    """
    https://www.etsy.com/developers/documentation/reference/listinginventory#method_getinventory
    """
    offering_id = models.BigIntegerField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    price_amount = models.PositiveIntegerField(null=True, blank=True, default=None)
    price_divisor = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    original_currency_code = models.CharField(max_length=3, null=True, blank=True, default=None)
