import warnings

from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.db.models.query import QuerySet
# from django.core.urlresolvers import reverse
from django.forms.widgets import Select, MultiWidget
# from django.utils.safestring import mark_safe


class BaseMultiSelect(MultiWidget):
    subwidget_choices = []

    class Media:
        js = ('multistep_select/multistep_select.js', )

    def __init__(self, attrs=None, **kwargs):
        """ The parameter `choices` is used here to set the instance attribute
            `subwidget_choices`, which is handled by the `choices` property
            and the `_get_choices` and `_set_choices` methods. """

        self.subwidget_choices = kwargs.get('choices')

        # Generate list of subwidgets.
        # `attrs` are passed down to individual subwidgets.
        subwidgets = tuple(
            self.get_subwidgets(attrs, self.get_subwidget_choices()))

        # Runs the base class constructor chain, passing the list of
        # subwidgets into MultiWidget.__init__, which makes sure any classes
        # in there are instantiated before calling Widget.__init__ - which
        # just initializes self.attrs = attrs.copy() or self.attrs = {}.
        super(BaseMultiSelect, self).__init__(subwidgets, attrs)

    def get_subwidgets(self, attrs, choices):
        """ Generate a list of subwidgets by appending a new Select to
            `widgets` # for each of the dataset provided in `choices`.
            QuerySets pass some special processing: their contents are zipped
            into lists of tuples ((pk1, object1), (pk2, object2)... (pkN,
                objectN)).


            Other dataset types are expected to conform to this format. """

        widgets = []

        for c in choices:
            if isinstance(c, QuerySet):
                """ Handle QuerySets passed as choice lists.
                    TODO: More robust handling of various iterables. """
                c = zip(c.values_list('pk', flat=True), c)
            widgets.append(Select(attrs=attrs, choices=c))
        return widgets

    def _set_choices(self, value):
        """ Perform the same list comprehension as in `MultiWidget.__init__`.
            We can't run the constructor itself here, though, since
            `Widget.__init__` nukes self.attrs. """

        try:
            new_widgets = [isinstance(w, type) and w() or w
                           for w in self.get_subwidgets(self.attrs, value)]
            self.subwidget_choices = value
            self.widgets = new_widgets
        except:
            # I have no idea what's going on here.
            warnings.warn("You are trying to set a BaseMultiSelect's"
                          " choices attribute to something other than a list"
                          " of choice lists. This action is ambiguous and is"
                          " only ignored because some of Django's built-in"
                          " form fields attempt to do the same.")

    def _get_choices(self):
        return self.subwidget_choices

    choices = property(_get_choices, _set_choices)

    def get_subwidget_choices(self):
        """ Returns a list of lists of possible choices for each
            subwidget. A likely most likely want to implement custom logic
            in this method to make widgets depend on each other by
            providing different available choices based on current
            values (see below for an example in SimpleFilterSelect). """

        return self.subwidget_choices

    def value_from_datadict(self, data, files, name):
        """ Given the data dict generated upon submitting the form,
            returns the final value of the widget based on dict entries
            that match the names of subwidgets. """

        raise NotImplemented("You need to implement the value_from_datadict"
                             " method in your subclass of BaseMultiSelect")

    def decompress(self, value):
        """ The opposite of value_from_datadict. Given the final value
            of the widget, determines what values should the individual
            subwidgets have. """

        raise NotImplemented("You need to implement the decompress method in"
                             " your subclass of BaseMultiSelect")


class SimpleFilterSelect(BaseMultiSelect):
    """ TODO: Abstract away from handling querysets, and use 3-tuples
              (value, text, relation_value) instead. This will also
              allow for code reuse between this and
              GenericRelationMultiSelect. QuerySets aren't the widget's job
              anyway.

        Implements one common use case for a multi-step select widget,
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
        """ In the context of this widget, the name and identifier `relation`
            is used for a string containing a related_name that returns
            a single Model instance; i.e. a OneToOne relation or a
            ForeignKey. """
        super(SimpleFilterSelect, self).__init__(attrs, **kwargs)

        # Get value for subwidget_relations and ensure there's the correct
        # count of relations defined.
        self.subwidget_relations = kwargs.pop('relations')
        if len(self.subwidget_relations) != len(self.subwidget_choices) - 1:
            error_text = "There must be %s relation(s) between %s subwidgets" \
                         " (%s given)" % (len(self.subwidget_choices) - 1,
                                          len(self.subwidget_choices),
                                          len(self.subwidget_relations))
            raise ImproperlyConfigured(error_text)

    def value_from_datadict(self, data, files, name):
        """ Allow each field to process its value on its own. Then, just
            return the value of the last one. """
        return [widget.value_from_datadict(data, files, name + '_%s' % i)
                for i, widget in enumerate(self.widgets)][-1]

    def decompress(self, value):
        """ The opposite of value_from_datadict. Determines what values
            should be displayed by the individual subwidgets, based on
            the final value alone. """

        """ So, we'll be iterating over relations in reverse order by
            popping the last elements off copies of the two lists. """
        relations = self.subwidget_relations[:]
        choice_lists = self.get_subwidget_choices()[:]
        
        """ If the value is None, return a list with as many `None`s
            as there are fields. """
        if value is None:
            return [None for _ in choice_lists]

        """ First of all, we get the last value and add it to the list. """
        values = [value]
        choices = choice_lists.pop()

        """ To determine the value for every next subwidget, we need
            to get the current object, and 'apply' the corresponding relation,
            i.e. retrieve the corresponding attribute. """
        while len(relations) > 0:
            relation = relations.pop()

            """ I'm not really sure how the following bit came to be.
                Lemme see if it works at all. """
            try:
                """ If choices is a QuerySet """
                obj = choices.get(pk=val)
                val = getattr(obj, relation)
            except AttributeError:
                """ If it's a list of tuples """
                pass
            values.insert(0, val)
            choices = choice_lists.pop()

        return values


class GenericRelationSelect(Select):
    """ Represents multiple sets of choices as <optgroup> elements
        within a single <select>. """

    def __init__(self, attrs=None, choices=(), placeholder='---------',
                 separator=','):
        super(Select, self).__init__(attrs)
        self.separator = separator
        self.placeholder = placeholder

        self.choices = list(choices)

    def get_format_string(self):
        return '%s' + self.separator + '%s'

    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        if len(value) != 0:
            # Group values by content type
            ctype_choices = value[0]
            obj_choices = value[1]

            value = ()
            for pk, ct in dict(ctype_choices).items():
                subchoices = ()
                for obj in [x for x in obj_choices
                            if isinstance(x[1], ct.model_class())]:
                    subchoice = (self.get_format_string() % (pk, obj[0]),
                                 obj[1])
                    subchoices += (subchoice, )
                value += ((ct, subchoices),)

        self._choices = value

    choices = property(_get_choices, _set_choices)

    def value_from_datadict(self, data, files, name):
        """ Takes a string (the value of the selected <option>, as
            taken from request variables) and returns a tuple of strings
            representing the ContentType and Model PKs. """

        value = super(GenericRelationSelect, self).value_from_datadict(data,
                                                                       files,
                                                                       name)
        try:
            v = value.split(self.separator, 1)
        except AttributeError:
            return [None, None]

        if len(v) < 2:
            return [None, None]

        return v

    def render(self, name, value, attrs=None, choices=()):
        """ TODO: Make sure that this method consistently receives the
            same type of value, preferably a tuple or list of pks, not
            a model instance. Model handling isn't the widget's job. """

        if isinstance(value, Model):
            value = self.get_format_string() % (
                ContentType.objects.get_for_model(value).pk,
                value.pk
            )
        elif not isinstance(value, list):
            value = []
        return super(GenericRelationSelect, self).render(name, value,
                                                         attrs, choices)

    def render_options(self, choices, selected_choices):
        """ Add placeholder for blank or optional fields. """

        try:
            selected_choices[0] = self.separator.join(selected_choices[0])
        except TypeError:
            selected_choices = [[None, None]]

        c = super(GenericRelationSelect, self).render_options(choices,
                                                              selected_choices)

        """ If we haven't selected anything yet, OR, if the field allows
            for selecting a null value, add a placeholder up front. """
        if selected_choices == [[None, None]] or not self.is_required:
            c = self.render_option(selected_choices, '', self.placeholder) + c
        return c


class GenericRelationMultiSelect(BaseMultiSelect):
    """ WIP: A two-element select widget to choose a ContentType and an ID.
        Works in conjunction with GenericRelationMultiSelect and
        GenericRelationFormMixin to provide better handling of
        GenericRelations in models. """

    def __init__(self, attrs=None, **kwargs):
        super(GenericRelationMultiSelect, self).__init__(attrs, **kwargs)

    def get_subwidget_choices(self):
        """ TODO: Return the list of models in one subwidget, and a
            corresponding queryset in the other. """
        return self.subwidget_choices

    def value_from_datadict(self, data, files, name):
        """ When queried, return a (ctype, id) tuple. """
        value = [widget.value_from_datadict(data, files, name + '_%s' % i)
                 for i, widget in enumerate(self.widgets)]
        return(value[-2], value[-1])

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
