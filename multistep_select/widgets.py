from django.core.urlresolvers import reverse
from django.forms.widgets import Select, MultiWidget
from django.utils.safestring import mark_safe


SELECT_SCRIPT = """"""


class TwoStepSelect(MultiWidget):

    class Media:
        js = ('multistep_select/multistep_select.js', )

    def __init__(self, attrs=None, **kwargs):
        self.parent_model = kwargs.get('parent_model')
        self.parent_choices = [('', '---')]
        self.parent_choices.extend(
            [(p.pk, p) for p in self.parent_model.objects.all()])

        self.child_model = kwargs.get('child_model')

        self.parent_lookup = kwargs.get('parent_lookup')
        self.child_lookup = kwargs.get('child_lookup')

        widgets = (
            Select(attrs=attrs, choices=self.parent_choices),
            Select(attrs=attrs, choices=[('', '---')])
        )
        super(TwoStepSelect, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        return data.get(name + "_1", None)

    def decompress(self, value):
        if value:
            try:
                child_instance = self.child_model.objects.get(pk=value)
                parent_instance = getattr(child_instance, self.parent_lookup)

                filter_kwargs = {self.parent_lookup: parent_instance}
                self.child_choices = [('', '---')]
                self.child_choices.extend([
                    (p.pk, p) for p in
                    self.child_model.objects.filter(**filter_kwargs)])

                self.widgets[1].choices = self.child_choices
                return [parent_instance.pk, child_instance.pk]
            except self.child_model.DoesNotExist:
                return [None, None]

        return [None, None]

    def render(self, name, value, attrs=None):
        if self.is_localized:
            for widget in self.widgets:
                widget.is_localized = self.is_localized

        if not isinstance(value, list):
            value = self.decompress(value)

        output = []
        final_attrs = self.build_attrs(attrs)

        id_ = final_attrs.get('id', None)

        widget_ids = []
        for i, widget in enumerate(self.widgets):
            widget_ids.append(id_ + name + '_%s' % i)
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(widget.render(name + '_%s' % i,
                                        widget_value,
                                        final_attrs))

        json_url = reverse(
            'json_list',
            kwargs={
                'app': self.child_model._meta.app_label,
                'model': self.child_model.__name__,
                'lookup': self.parent_lookup,
                'value': "$VALUE$"
            }
        )


        out_script = SELECT_SCRIPT % {'id': id_, 'url': json_url}

        output.append(out_script)

        return mark_safe(self.format_output(output))
