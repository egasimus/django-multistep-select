from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from .models import *
from .forms import *


class Home(TemplateView):
    template_name = 'index.html'


class SimpleListMixin(object):
    def get_context_data(self, **kwargs):
        d = super(SimpleListMixin, self).get_context_data(**kwargs)
        d.update({'object_list': self.model.objects.all(),
                  'object_name': self.model._meta.verbose_name.title(),
                  'object_field': self.model.get_second_field_name()})
        return d


class SimpleFooCreate(SimpleListMixin, CreateView):
    template_name = 'form.html'
    model = SimpleFoo
    form_class = SimpleFooForm
    success_url = reverse_lazy('simple')


class FilterBarMixin(SimpleListMixin):
    template_name = 'form.html'
    model = FilterBar
    form_class = FilterBarForm
    success_url = reverse_lazy('filter')


class FilterBarCreate(FilterBarMixin, CreateView): pass


class FilterBarUpdate(FilterBarMixin, UpdateView): pass


class GenericBazMixin(SimpleListMixin):
    template_name = 'form.html'
    model = GenericBaz
    form_class = GenericBazForm
    success_url = reverse_lazy('generic')


class GenericBazCreate(GenericBazMixin, CreateView): pass


class GenericBazUpdate(GenericBazMixin, UpdateView): pass
