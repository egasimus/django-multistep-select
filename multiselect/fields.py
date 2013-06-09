from itertools import chain

from django.contrib.contenttypes.models import ContentType
from django.forms.fields import ChoiceField

from .widgets import GenericRelationMultiSelect


class GenericRelationField(ChoiceField):
    ct_field = 'content_type'
    fk_field = 'object_id'
    widget = GenericRelationMultiSelect

    def __init__(self, choices, *args, **kwargs):
        self.ct_field = kwargs.pop('ct_field', self.ct_field)
        self.fk_field = kwargs.pop('fk_field', self.fk_field)

        super(GenericRelationField, self).__init__(*args, **kwargs)

        self.choices = choices

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        ctype_choices = [(
            ContentType.objects.get_for_model(x.model).pk,
            ContentType.objects.get_for_model(x.model)
        ) for x in value]
        object_choices = list(
            chain(*[zip(x.values_list('pk', flat=True), x) for x in value])
        )

        self._choices = self.widget.choices = (
            ctype_choices,
            object_choices
        )

    choices = property(_get_choices, _set_choices)

    def to_python(self, value):
        if None in value:
            return None
        ct = ContentType.objects.get_for_id(value[-2])
        return [ct, ct.model_class().objects.get(pk=value[-1])]

    def valid_value(self, value):
        for x, v in enumerate(value):
            if v not in [y[1] for y in self.choices[x]]:
                return False
        return True
