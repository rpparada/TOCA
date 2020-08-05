from django import forms

from .models import Direccion

class DireccionForm(forms.ModelForm):

    class Meta:
        model = Direccion
