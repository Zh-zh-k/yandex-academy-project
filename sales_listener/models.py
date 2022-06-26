from django.conf import settings
from django.db import models
from django.utils import timezone


class Position(models.Model):
    available_types = (("OFFER", "OFFER"), ("CATEGORY", "CATEGORY"))
    id = models.TextField(primary_key=True, editable=False)
    parentId = models.TextField(null=True)
    name = models.TextField()
    date = models.TextField()
    type = models.TextField(choices=available_types)
    price = models.BigIntegerField(null=True)
    #children = models.ManyToManyField("self")

