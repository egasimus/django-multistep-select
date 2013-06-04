from itertools import chain

from django.contrib.contenttypes.models import ContentType
from django.forms.fields import Field, ChoiceField
from django.utils.encoding import smart_text

from .widgets import GenericRelationWidget


class GenericRelationField(ChoiceField):
    ct_field = 'content_type'
    id_field = 'object_id'
    widget = GenericRelationWidget

    def __init__(self, choices, *args, **kwargs):
        self.ct_field = kwargs.pop('ct_field', self.ct_field)
        self.id_field = kwargs.pop('id_field', self.id_field)

        super(GenericRelationField, self).__init__(*args, **kwargs)

        self.choices = choices
        self.widget = GenericRelationWidget(choices=self.choices)

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        ctype_choices = [(
            ContentType.objects.get_for_model(x.model).pk,
            ContentType.objects.get_for_model(x.model)
        ) for x in value]
        object_choices = \
            chain(*[zip(x.values_list('pk', flat=True), x) for x in value])

        self._choices = self.widget.choices = (
            ctype_choices,
            object_choices
        )

        print self._choices

    choices = property(_get_choices, _set_choices)

    def to_python(self, value):
        return [ContentType.objects.get_for_id(value[-2]), value[-1]]

    def valid_value(self, value):
        valid = False

        for n, val in enumerate(value):
            for k, v in self.choices[n]:
                if val == smart_text(k):
                    valid = True
                else:
                    return False

        return valid
