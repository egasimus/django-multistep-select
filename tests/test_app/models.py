from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class SimpleFoo(models.Model):
    name = models.CharField(max_length=50)

    RED = 0
    GREEN = 1
    BLUE = 2
    COLORS = [(RED, 'Red'),
              (GREEN, 'Green'),
              (BLUE, 'Blue')]
    color = models.PositiveSmallIntegerField(blank=True, null=True,
                                             choices=COLORS)

    def get_second_field_name(self):
        return 'Color'

    def get_second_field_display(self):
        return self.get_color_display()


class FilterBar(models.Model):
    name = models.CharField(max_length=50)
    foo = models.ForeignKey(SimpleFoo)

    def get_second_field_name(self):
        return 'Related Foo'

    def get_second_field_display(self):
        return unicode(self.foo)


class GenericBaz(models.Model):
    name = models.CharField(max_length=50)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def get_second_field_name(self):
        return 'Related Object'

    def get_second_field_display(self):
        return unicode(self.content_object)
