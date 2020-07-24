from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario, UsuarioArtista
from artista.models import Artista

from toca.parametros import parUsuarioArtistas

class IngresarForm(forms.Form):

    nombreusuario   = forms.CharField(widget=forms.TextInput(attrs={
                                                                "id": "primercampo",
                                                                "class": "form-control",
                                                                "placeholder": "Email"
                                                            }), label=''
                                    )
    contra          = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "id": "contra",
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña"
                                                            }), label=''
                                    )

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
        fields = ('rut','digitoVerificador','banco','num_celular','num_cuenta','tipo_cuenta')

class AgregaCamposUsuarioArtForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','email','password1','password2','first_name','last_name')

class ArtistaForm(forms.ModelForm):

    class Meta:
        model = Artista
        fields = ('id','email')
