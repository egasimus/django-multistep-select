from itertools import chain

from django.contrib.contenttypes.models import ContentType
from django.forms.fields import Field
from multistep_select.widgets import GenericRelationWidget


class GenericRelationField(Field):
    def __init__(self, choices, ct_field='content_type', id_field='object_id',
                 *args, **kwargs):

        self.ct_field = ct_field
        self.id_field = id_field

        ctype_choices = [(
            ContentType.objects.get_for_model(x.model).pk,
            ContentType.objects.get_for_model(x.model)
        ) for x in choices]
        object_choices = \
            chain(*[zip(x.values_list('pk', flat=True), x) for x in choices])
        widget_choices = (
            ctype_choices,
            object_choices
        )
        self.widget = GenericRelationWidget(choices=widget_choices)

        super(GenericRelationField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        return [ContentType.objects.get_for_id(value[-2]), value[-1]]
