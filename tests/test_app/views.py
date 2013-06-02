from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView
from .models import *


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
    success_url = reverse_lazy('simple')


class FilterBarCreate(SimpleListMixin, CreateView):
    template_name = 'form.html'
    model = FilterBar


class GenericBazCreate(SimpleListMixin, CreateView):
    template_name = 'form.html'
    model = GenericBaz
