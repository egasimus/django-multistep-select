from django.contrib.contenttypes.generic import GenericForeignKey

from .fields import GenericRelationField


class GenericRelationModelFormMixin(object):
    """ The django.contrib.contenttypes.generic.GenericForeignKey
        'pseudo-field' superficially resembles, but in fact is not a
        model field; as the Django documentation points out, it is
        internally represented by two separate model fields, commonly
        named 'content_type' and 'object_id'.

        By design, form fields are not aware of each other, or of their
        parent form, which is why implementing a form field that sets
        the value of two model fields requires manipulation at the Form
        level in addition to implementing a suitable Field and Widget.

        This mixin serves the simple purpose of breaking down the
        (ctype, id) 2-tuples returned by GenericRelationField.to_python
        into individual values, and making sure the form passes them to
        the model as usual. """

    def _initialize(self):
        try:
            for field in self.instance._meta.virtual_fields:
                if isinstance(field, GenericForeignKey):
                    self.initial.update({
                        field.name: getattr(self.instance, field.name),
                    })
        except AttributeError:
            """ Ignore instance initialization if the mixin is used with
                a non-model Form."""
            pass

    def __init__(self, *args, **kwargs):
        super(GenericRelationModelFormMixin, self).__init__(*args, **kwargs)
        self._initialize()

    def _split_generic_fields(self, cleaned_data):
        for name, field in self.fields.items():
            if (
                isinstance(field, GenericRelationField)
                and name in cleaned_data
            ):
                cleaned_data.update({
                    field.ct_field: cleaned_data[name][0],
                    field.fk_field: cleaned_data[name][1].pk
                })
                self._meta.fields += (field.ct_field, field.fk_field)
                del cleaned_data[name]
        return cleaned_data

    def clean(self):
        cleaned_data = super(GenericRelationModelFormMixin, self).clean()
        return self._split_generic_fields(cleaned_data)
