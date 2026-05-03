from django.contrib.postgres.fields import ArrayField
from django.db import models

class IPhone(models.Model):
    full_name = models.CharField(max_length=512)
    color = models.CharField(max_length=64)
    storage = models.CharField(max_length=16)
    producer = models.CharField(max_length=64)
    default_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True, blank=True)
    exist = models.BooleanField(default=False)
    image_list = ArrayField(models.URLField(max_length=512), default=list)
    product_code = models.CharField(max_length=32)
    feedback_count = models.PositiveIntegerField(default=0)
    diagonal = models.DecimalField(max_digits=3, decimal_places=1)
    pixels = models.CharField(max_length=32)
    details = models.JSONField(default=dict)
