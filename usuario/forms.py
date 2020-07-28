from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario, UsuarioArtista
from artista.models import Artista

from toca.parametros import parUsuarioArtistas

class IngresarForm(forms.Form):

    nombreusuario   = forms.EmailField(widget=forms.EmailInput(attrs={
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

class UserForm(UserCreationForm):

    email           = forms.EmailField(widget=forms.EmailInput(attrs={
                                                                "id": "primercampo",
                                                                "class": "form-control",
                                                                "placeholder": "Email"
                                                            }), label='Email'
                                    )
    password1       = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña"
                                                            }), label='Contraseña'
                                    )
    password2       = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña"
                                                            }), label='Repite Contraseña'
                                    )

    class Meta:
        model = User
        fields = ('email','password1','password2')

class UsuarioArtistaForm(forms.ModelForm):

    rut                 = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                'id': 'rut',
                                                                'class': 'form-control',
                                                                'placeholder': 'RUT'
                                                            }), label='RUT'
                                        )
    digitoVerificador   = forms.CharField(max_length=1, widget=forms.TextInput(attrs={
                                                                'id': 'digitover',
                                                                'class': 'form-control',
                                                                'placeholder': 'Digito Ver.'
                                                            }), label='Digito Verificador'
                                        )
    num_celular         = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Número Celular'
                                                            }), label='( +56 ) 9'
                                        )
    banco               = forms.ChoiceField(choices=parUsuarioArtistas['bancos'],
                                                    widget=forms.Select(attrs={
                                                                        'class': 'form-control',
                                                                        }), label='Banco'
                                    )
    num_cuenta          = forms.CharField(widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Número Cuenta'
                                                            }), label='Número Cuenta'
                                        )
    tipo_cuenta         = forms.ChoiceField(choices=parUsuarioArtistas['tipo_cuenta'],
                                                    widget=forms.Select(attrs={
                                                                        'class': 'form-control',
                                                                        }), label='Tipo Cuenta'
                                    )

    class Meta:
        model = UsuarioArtista
        fields = ('rut',
                'digitoVerificador',
                'banco',
                'num_celular',
                'num_cuenta',
                'tipo_cuenta',
                'artista')

        widgets = {
            'artista': forms.HiddenInput(),
        }

class ArtistaUserForm(UserCreationForm):

    email           = forms.EmailField(widget=forms.EmailInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Email",
                                                                'readonly': 'readonly'
                                                            }), label='Email'
                                    )
    password1       = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña"
                                                            }), label='Contraseña'
                                    )
    password2       = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña"
                                                            }), label='Repite Contraseña'
                                    )
    first_name          = forms.CharField(widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre'
                                                            }), label='Nombre'
                                        )
    last_name          = forms.CharField(widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Apellido'
                                                            }), label='Apellido'
                                        )

    class Meta:
        model = User
        fields = ('email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'username')

        widgets = {
            'username': forms.HiddenInput(),
        }

class EditarCuentaUserForm(forms.ModelForm):

    email               = forms.EmailField(widget=forms.EmailInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Email",
                                                                'readonly': 'readonly'
                                                            }), label='Email'
                                    )
    first_name          = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre'
                                                            }), label='Nombre'
                                        )
    last_name           = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Apellido'
                                                            }), label='Apellido'
                                        )

    class Meta:
        model = User
        fields = ('email','first_name','last_name')
