from django import forms

from .models import Tocata

class TocataForm(forms.ModelForm):

    hora = forms.TimeField(input_formats=['%H:%M', '%I:%M%p', '%I:%M %p'])

    class Meta:
        model = Tocata
        fields = '__all__'
