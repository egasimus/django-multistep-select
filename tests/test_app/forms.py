from django import forms

from .models import *
from multistep_select.widgets import SimpleFilterSelect


class SimpleFooForm(forms.ModelForm):
    class Meta:
        model = SimpleFoo
        fields = ('name', 'color')


class FilterBarForm(forms.ModelForm):
    class Meta:
        model = FilterBar
        fields = ('name', )

    foo = forms.ModelChoiceField(
        widget=SimpleFilterSelect(names=['colorpick', 'foo'],
                                  choices=[SimpleFoo.COLORS,
                                               SimpleFoo.objects.all()],
                                  relations=['color']),
        queryset=SimpleFoo.objects.all()
    )


class GenericBazForm(forms.ModelForm):
    class Meta:
        model = GenericBaz
        fields = ('name', )
