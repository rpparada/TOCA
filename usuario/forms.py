from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario, UsuarioArtista

from toca.parametros import parUsuarioArtistas

class AgregaCamposUsuarioForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('es_artista',)

class UsuarioArtistaForm(forms.ModelForm):

    class Meta:
        model = UsuarioArtista
        fields = ('rut','digitoVerificador','banco','artista','num_celular','num_cuenta','tipo_cuenta')

    def __init__(self, *args, **kwargs):
        super(UsuarioArtistaForm, self).__init__(*args, **kwargs)
        self.fields['artista'].empty_label = None