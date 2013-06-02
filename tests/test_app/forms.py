from django.forms import ModelForm
from .models import *


class SimpleFooForm(ModelForm):
    class Meta:
        model = SimpleFoo
        fields = ('name', 'color')


class FilterBarForm(ModelForm):
    class Meta:
        model = FilterBar
        fields = ('name', 'foo')


class GenericBazForm(ModelForm):
    class Meta:
        model = GenericBaz
        fields = ('name', )
