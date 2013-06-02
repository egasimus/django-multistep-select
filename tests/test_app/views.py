from django.views.generic import TemplateView, CreateView
from .models import *


class Home(TemplateView):
    template_name = 'index.html'


class JustFooCreate(CreateView):
    template_name = 'form_justfoo.html'
    model = JustFoo


class FilterBarCreate(CreateView):
    template_name = 'form_filterbar.html'
    model = FilterBar


class GenericBazCreate(CreateView):
    template_name = 'form_genericbaz.html'
    model = GenericBaz
