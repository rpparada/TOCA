from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario

class AgregaCamposUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('es_artista',)
