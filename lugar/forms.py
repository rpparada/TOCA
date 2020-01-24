from django import forms
from .models import Lugar, Region, Provincia, Comuna

class AgregarForm(forms.ModelForm):

    class Meta():
        model = Lugar
        exclude = ['usuario','fecha_crea','fecha_actua','provincia','estado']

class EditarForm(forms.ModelForm):

    class Meta():
        model = Lugar
        exclude = ['usuario','fecha_crea','fecha_actua','provincia','estado']
