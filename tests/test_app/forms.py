from django import forms

from .models import *
from multistep_select.fields import GenericRelationField
from multistep_select.forms import GenericRelationFormMixin
from multistep_select.widgets import SimpleFilterSelect


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


class GenericBazForm(GenericRelationFormMixin, forms.ModelForm):
    class Meta:
        model = GenericBaz
        fields = ('name', 'content_object')

    content_object = GenericRelationField(choices=[
        FilterBar.objects.all(),
        SimpleFoo.objects.all(),
        GenericBaz.objects.all()
    ])
