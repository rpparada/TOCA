from django import forms

from .models import LugaresTocata

class LugaresTocataForm(forms.ModelForm):

    class Meta:
        model = LugaresTocata
        exclude = ('fecha_actu','fecha_crea','estado')
