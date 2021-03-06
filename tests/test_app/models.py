from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.db import models


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

    @classmethod
    def get_second_field_name(cls):
        return 'Color'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.get_color_display())

    def get_second_field_display(self):
        return self.get_color_display()

    def get_absolute_url(self):
        return reverse('simple_edit', kwargs={'pk': self.pk})


class FilterBar(models.Model):
    name = models.CharField(max_length=50)
    foo = models.ForeignKey(SimpleFoo)

    @classmethod
    def get_second_field_name(cls):
        return 'Related Foo'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.foo)

    def get_second_field_display(self):
        return unicode(self.foo)

    def get_absolute_url(self):
        return reverse('filter_edit', kwargs={'pk': self.pk})


class GenericBaz(models.Model):
    name = models.CharField(max_length=50)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    @classmethod
    def get_second_field_name(cls):
        return 'Related Object'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.content_object)

    def get_second_field_display(self):
        return unicode(self.content_object)

    def get_absolute_url(self):
        return reverse('generic_edit', kwargs={'pk': self.pk})
