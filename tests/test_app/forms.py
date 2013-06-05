from django import forms

from .models import *
from multiselect.fields import GenericRelationField
from multiselect.forms import GenericRelationModelFormMixin
from multiselect.widgets import SimpleFilterSelect, GenericRelationSelect


class SimpleFooForm(forms.ModelForm):
    class Meta:
        model = SimpleFoo
        fields = ('name', 'color')


class FilterBarForm(forms.ModelForm):
    class Meta:
        model = FilterBar
        fields = ('name', 'foo')

    foo = forms.ModelChoiceField(
        widget=SimpleFilterSelect(choices=[SimpleFoo.COLORS,
                                           SimpleFoo.objects.all()],
                                  relations=['color']),
        queryset=SimpleFoo.objects.all()
    )


class GenericBazForm(GenericRelationModelFormMixin, forms.ModelForm):
    class Meta:
        model = GenericBaz
        fields = ('name', 'content_object')

    content_object = GenericRelationField(widget=GenericRelationSelect,
                                          choices=[FilterBar.objects.all(),
                                                   SimpleFoo.objects.all(),
                                                   GenericBaz.objects.all()])
