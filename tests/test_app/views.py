from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from .models import *
from .forms import *


class Home(TemplateView):
    template_name = 'index.html'


class SimpleListMixin(object):
    def get_context_data(self, **kwargs):
        d = super(SimpleListMixin, self).get_context_data(**kwargs)
        d.update({'show_object_list': True,
                  'object_list': self.model.objects.all(),
                  'object_name': self.model._meta.verbose_name.title(),
                  'object_field': self.model.get_second_field_name()})
        return d


class SimpleFooMixin(object):
    template_name = 'form.html'
    model = SimpleFoo
    form_class = SimpleFooForm
    success_url = reverse_lazy('simple')


class SimpleFooCreate(SimpleFooMixin, SimpleListMixin, CreateView): pass


class SimpleFooUpdate(SimpleFooMixin, UpdateView): pass


class FilterBarMixin(object):
    template_name = 'form.html'
    model = FilterBar
    form_class = FilterBarForm
    success_url = reverse_lazy('filter')


class FilterBarCreate(FilterBarMixin, SimpleListMixin, CreateView): pass


class FilterBarUpdate(FilterBarMixin, UpdateView): pass


class GenericBazMixin(object):
    template_name = 'form.html'
    model = GenericBaz
    form_class = GenericBazForm
    success_url = reverse_lazy('generic')


class GenericBazCreate(GenericBazMixin, SimpleListMixin, CreateView): pass


class GenericBazUpdate(GenericBazMixin, UpdateView): pass
