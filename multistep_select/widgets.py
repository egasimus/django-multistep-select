# from django.core.exceptions import ImproperlyConfigured
# from django.core.urlresolvers import reverse
from django.forms.widgets import Select, MultiWidget
# from django.utils.safestring import mark_safe


class BaseMultiStepSelect(MultiWidget):
    subwidget_choices = []
    subwidget_names = []

    class Media:
        js = ('multistep_select/multistep_select.js', )

    def __init__(self, attrs=None, **kwargs):
        self.subwidget_choices = self.get_subwidget_choices()
        self.subwidget_names = self.get_subwidget_names()

        widgets = []
        for choices in self.subwidget_choices:
            widgets.append(Select(attrs=attrs, choices=choices))

        super(BaseMultiStepSelect, self).__init__(tuple(widgets), attrs)

    def get_subwidget_choices(self):
        """ Returns a list of lists of possible choices for each
            subwidget. You'll most likely want to implement custom logic
            in this method to make widgets interdependent (see below
            for an example in FilterMultiStepSelect). """

        return self.subwidget_choices

    def get_subwidget_names(self):
        """ Implementing this method allows for generating subwidget
            names on the fly. For example, one can  """

        return self.subwidget_names

    def value_from_datadict(self, data, files, name):
        """ Given a data dict matching the names and values of submitted
            data, returns the final value of the widget. """

        raise NotImplemented("You need to implement the value_from_datadict"
                             " method of this MultiStepSelect.")

    def decompress(self, value):
        """ The opposite of value_from_datadict. Given the final value
            of the widget, determines what values should the individual
            subwidgets have. """

        raise NotImplemented("You need to implement the decompress method of"
                             " this MultiStepSelect.")



class FilterMultiStepSelect(BaseMultiStepSelect):

    def decompress(self, value):
        """ The opposite of value_from_datadict. Given the final value
            of the widget, determines what values should the individual
            subwidgets have. """

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
