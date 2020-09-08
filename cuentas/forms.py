# cuentas.forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages, auth

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

from .tokens import account_activation_token, art_activation_token

from .models import EmailActivation
from artista.models import Artista
from perfil.models import PerfilUser, PerfilArtista

from .signals import user_logged_in

from perfil.models import BANCOS_OPCIONES, TIPOS_CUENTAS_OPCIONES

class ReactivateEmailForm(forms.Form):
    email           = forms.EmailField(widget=forms.EmailInput(attrs={
                                                                "id": "id_email",
                                                                "class": "form-control",
                                                                "placeholder": "Ingresa tu email...",
                                                                "class": "form-control form-white placeholder"
                                                            }), label='Email'
                                    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse('cuenta:registrar')
            msg = '''Email no existe, ¿Te gustaria <a href="{link}">registrarte</a>?
            '''.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email

class CuentaSetPasswordForm(SetPasswordForm):
    new_password1   = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Nueva Contraseña",
                                                                "autofocus": True
                                                            }), label='Nueva Contraseña'
                                    )
    new_password2   = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Repite Nueva Contraseña"
                                                            }), label='Repite Nueva Contraseña'
                                    )

class CuentaPasswordResetForm(PasswordResetForm):
    email           = forms.EmailField(widget=forms.EmailInput(attrs={
                                                                "id": "id_email",
                                                                "class": "form-control",
                                                                "placeholder": "Ingresa tu email...",
                                                                "class": "form-control form-white placeholder"
                                                            }), label='Email'
                                    )

class CuentaPasswordChangeForm(PasswordChangeForm):

    old_password    = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "id": "primercampo",
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña Actual",
                                                                "autofocus": True
                                                            }), label='Contraseña Actual'
                                    )
    new_password1   = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Nueva Contraseña"
                                                            }), label='Nueva Contraseña'
                                    )
    new_password2   = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Repite Nueva Contraseña"
                                                            }), label='Repite Nueva Contraseña'
                                    )

User = get_user_model()

class IngresarForm(forms.Form):

    email           = forms.EmailField(widget=forms.EmailInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Email",
                                                                "autofocus": True
                                                            }), label=''
                                    )
    contra          = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "id": "contra",
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña"
                                                            }), label=''
                                    )
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(IngresarForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data

        email = data.get('email')
        contra = data.get('contra')

        qs = User.objects.filter(email=email)
        if qs.exists():
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                link = reverse('cuenta:resent-activation')
                reconfirm_msg = '''Ve a <a href="{resend_link}">
                reenviar email de conformacion</a>.
                '''.format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = 'Por favor, revisa tu correo para validar tu cuenta o '+reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = 'Email no confirmado'+reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and not email_confirm_exists:
                    raise forms.ValidationError('Este usuario esta inactivo')

        usuario = auth.authenticate(username=email, password=contra)
        if usuario is None:
            raise forms.ValidationError('Credenciales Invalidas')
        auth.login(request, usuario)
        self.user = usuario
        user_logged_in.send(usuario.__class__, instance=usuario, request=request)

        return data

class RegistrarUserForm(forms.ModelForm):

    email           = forms.EmailField(widget=forms.EmailInput(attrs={
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
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Contraseñas deben ser iguales")
        return password2

    def save(self, commit=True):
        user = super(RegistrarUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False

        if commit:
            user.save()
        return user

class UserAdminCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserDetailChangeViewForm(forms.ModelForm):

    nombre          = forms.CharField(widget=forms.TextInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Nombre"
                                                            }), label='Nombre', required = False
                                    )
    apellido        = forms.CharField(widget=forms.TextInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Apellido"
                                                            }), label='Apellido', required=False
                                    )

    class Meta:
        model = User
        fields = ('nombre','apellido')

class UserAdminChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'admin')

    def clean_password(self):
        return self.initial["password"]

class EnviaEmailNuevoArtistaForm(forms.Form):

    artista         = forms.ModelChoiceField(
                        queryset=Artista.objects.filter(usuario__isnull=True),
                        #empty_label=None
                        empty_label='Selecciona Artista'
                    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(EnviaEmailNuevoArtistaForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        artista = data.get('artista')

        if artista.email:
            current_site = get_current_site(request)
            mail_subject = 'Formulario de Ingreso de Artistas a Tocatas Intimas.'
            message = render_to_string('cuentas/email_nuevo_artista_cuenta.html', {
                'user': artista,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(artista.pk)),
                'token': art_activation_token.make_token(artista),
            })
            to_email = artista.email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Formulario Enviado')
        else:
            raise forms.ValidationError("Artista no tiene email registrado")

        return data

class RegistrarArtistaForm(forms.Form):

    email               = forms.EmailField(widget=forms.EmailInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Email",
                                                                'readonly': 'readonly'
                                                            }), label='Email'
                                    )
    password1           = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña"
                                                            }), label='Contraseña'
                                    )
    password2           = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña"
                                                            }), label='Repite Contraseña'
                                    )
    nombre              = forms.CharField(widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre',
                                                                'autofocus': True
                                                            }), label='Nombre'
                                        )
    apellido            = forms.CharField(widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Apellido'
                                                            }), label='Apellido'
                                        )
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
    banco               = forms.ChoiceField(choices=BANCOS_OPCIONES,
                                                    widget=forms.Select(attrs={
                                                                        'class': 'form-control',
                                                                        }), label='Banco'
                                    )
    num_cuenta          = forms.CharField(widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Número Cuenta'
                                                            }), label='Número Cuenta'
                                        )
    tipo_cuenta         = forms.ChoiceField(choices=TIPOS_CUENTAS_OPCIONES,
                                                    widget=forms.Select(attrs={
                                                                        'class': 'form-control',
                                                                        }), label='Tipo Cuenta'
                                    )
    artista             = forms.ModelChoiceField(
                                queryset=Artista.objects.filter(usuario__isnull=True),
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        print(request)
        super(RegistrarArtistaForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data

        # Data user
        email = data.get('email')
        contra = data.get('password1')

        user = User.objects.create_musico(
                                    email=email,
                                    password=contra
                                )

        # Data PerfilUser
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        user_perfil = PerfilUser.objects.create_perfiluser(
                                                    user=user,
                                                    nombre=nombre,
                                                    apellido=apellido
                                                )

        # Data PerfilArtista
        rut = data.get('rut')
        digitoVerificador = data.get('digitoVerificador')
        num_celular = data.get('num_celular')
        banco = data.get('banco')
        num_cuenta = data.get('num_cuenta')
        tipo_cuenta = data.get('tipo_cuenta')

        user_perfil_artista = PerfilArtista.objects.create_perfilartista(
                                                    user=user,
                                                    rut=rut,
                                                    digitoVerificador=digitoVerificador,
                                                    num_celular=num_celular,
                                                    banco=banco,
                                                    num_cuenta=num_cuenta,
                                                    tipo_cuenta=tipo_cuenta
                                                )
        # Data Artista
        artista = data.get('artista')
        artista.link_user(user)

        # Ingresa artista
        auth.login(request, user)
        self.user = user
        user_logged_in.send(user.__class__, instance=user, request=request)
        messages.success(request, 'Registro existoso')

        return data

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Contraseñas deben ser iguales")
        return password2
