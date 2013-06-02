from django.core.exceptions import ImproperlyConfigured
# from django.core.urlresolvers import reverse
from django.forms.widgets import Select, MultiWidget
# from django.utils.safestring import mark_safe


class BaseMultiStepSelect(MultiWidget):
    subwidget_names = []
    subwidget_choices = []

    class Media:
        js = ('multistep_select/multistep_select.js', )

    def __init__(self, attrs=None, **kwargs):
        self.subwidget_names = kwargs.pop('names', self.subwidget_names)
        self.subwidget_choices = kwargs.pop('choices', self.subwidget_choices)

        widgets = []
        for choices in self.get_subwidget_choices():
            widgets.append(Select(attrs=attrs, choices=choices))
        super(BaseMultiStepSelect, self).__init__(tuple(widgets), attrs)

    def get_subwidget_choices(self):
        """ Returns a list of lists of possible choices for each
            subwidget. You'll most likely want to implement custom logic
            in this method to make widgets depend on each other by
            providing different available choices based on current
            values (see below for an example in SimpleFilterSelect). """

        return self.subwidget_choices

    def get_subwidget_names(self):
        """ Implementing this method allows for generating subwidget
            names on the fly. """

        return self.subwidget_names

    def value_from_datadict(self, data, files, name):
        """ Given the data dict generated upon submitting the form,
            returns the final value of the widget based on dict entries
            that match the names of subwidgets. """

        raise NotImplemented("You need to implement the value_from_datadict"
                             " method in your subclass of BaseMultiStepSelect")

    def decompress(self, value):
        """ The opposite of value_from_datadict. Given the final value
            of the widget, determines what values should the individual
            subwidgets have. """

        raise NotImplemented("You need to implement the decompress method in"
                             " your subclass of BaseMultiStepSelect")



class SimpleFilterSelect(BaseMultiStepSelect):
    """ Implements one common use case for a multi-step select widget,
        allowing the user to filter through a multitude of choices by
        traversing a tree-like path:

        * Each <select> SHALL allow for selecting a single item.
          The user SHALL progress through the <select>s in linear order.
        * Each <select> SHALL remain blank until the one preceding it is
          filled in.
        * When a <select> is filled in, the next one SHALL be populated
          with a list of values filtered based on the value of the
          preceding <select>.
        * When the last <select> is filled in, the value of the widget
          SHALL be made equal to the value of the last <select>.

          For this filtering to work in an unambiguous manner, this
          widget must work subject to the following conditions:

        * The item in the 'subwidget_choices' list that corresponds to
          each <select> MUST be a list of instances of a single model;
          with the exception of the first <select>, whose choices MAY
          instead be given in any format supported by Django's Select
          widget.
        * Thus, we can say that each <select> except for the first one
          SHALL be matched to a single Model.
        * Each <select> SHALL have a relation to the next one. A
          relation is a field of the next <select>'s model. The name of
          a <select>'s relation is specified in 'subwidget_relations'.
        * When a <select> is filled in, the next one SHALL be populated
          with those items from its corresponding queryset (as listed in
          'subwidget_choices'), whose relation field value equals the
          value of the <select> that has been just filled in.
        * This is with the exception of the last <select>, which has
          nothing to filter, and instead SHALL represent the final value
          of this widget. """

    subwidget_relations = []

    def __init__(self, attrs=None, **kwargs):
        super(SimpleFilterSelect, self).__init__(attrs, **kwargs)

        if len(self.subwidget_choices) != len(self.subwidget_names):
            raise ImproperlyConfigured("List of names doesn't correspond to"
                                       " list of lists of choices.")

        self.subwidget_relations = \
            kwargs.pop('relations', self.subwidget_relations)

        if len(self.subwidget_relations) != len(self.subwidget_choices) - 1:
            error_text = "There must be %s relation(s) between %s subwidgets" \
                         " (%s given)" % (len(self.subwidget_choices) - 1,
                                          len(self.subwidget_choices),
                                          len(self.subwidget_relations))
            raise ImproperlyConfigured(error_text)

    def decompress(self, value):
        """ The opposite of value_from_datadict. Given the final value
            of the widget, determines what values should be displayed by
            the individual subwidgets. """

        values = []

        """ If the value is None, fill the values list with as many
            None's as there are fields. """
        if value is None:
            for _ in range(0, len(self.get_subwidget_choices())):
                values.append(None)
            return values

        """ We'll be iterating over relations in reverse order. """
        relations = self.subwidget_relations[:]
        relations.reverse()
        choice_lists = self.get_subwidget_choices()[:]
        choice_lists.reverse()

        """ On the first iteration, we get the last value and add it to
            the list. """
        val = value
        values.insert(0, val)

        while len(relations) > 0:
            """ To determine the value for the next subwidget, we need
                to get the current object, and look at the value of its
                relation field. """
            choices = choice_lists.pop()
            relation = relations.pop()
            try:
                obj = choices.get(pk=value)
                val = getattr(obj, relation)
            except AttributeError:
                val = dict(choices).get(value)
            values.insert(0, val)

        return values
