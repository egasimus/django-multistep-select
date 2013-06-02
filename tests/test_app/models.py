from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class JustFoo(models.Model):
    name = models.CharField(max_length=50)

    RED = 0
    GREEN = 1
    BLUE = 2
    COLORS = [(RED, 'Red'),
              (GREEN, 'Green'),
              (BLUE, 'Blue')]
    color = models.PositiveSmallIntegerField(blank=True, null=True,
                                             choices=COLORS)


class FilterBar(models.Model):
    name = models.CharField(max_length=50)
    foo = models.ForeignKey(JustFoo)


class GenericBaz(models.Model):
    name = models.CharField(max_length=50)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    foo = generic.GenericForeignKey()
