# cuentas.forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages, auth

from .models import EmailActivation

from .signals import user_logged_in

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
                                                                "placeholder": "Nueva Contraseña"
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
                                                                "placeholder": "Contraseña Actual"
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
                                                                "id": "primercampo",
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

    # def form_valid(self, form):
    #     request = self.request
    #     next_ = request.GET.get('next')
    #     next_post = request.POST.get('next')
    #     redirect_path = next_ or next_post or None
    #
    #     email = form.cleaned_data.get('email')
    #     contra = form.cleaned_data.get('contra')
    #     usuario = auth.authenticate(username=email, password=contra)
    #     if usuario is not None:
    #         if not usuario.is_active:
    #             messages.error(request,'Usuario Inactivo')
    #             return super(IngresarView, self).form_invalid(form)
    #
    #         auth.login(request, usuario)
    #         user_logged_in.send(usuario.__class__, instance=usuario, request=request)
    #         #if Usuario.objects.get(user=usuario).es_artista:
    #         #    request.session['es_artista'] = 'S'
    #         #else:
    #         #    request.session['es_artista'] = 'N'
    #         messages.success(request,'Ingreso Existos')
    #         if is_safe_url(redirect_path, request.get_host()):
    #             return redirect(redirect_path)
    #         else:
    #             return redirect('/')
    #     return super(IngresarView, self).form_invalid(form)

class RegistrarUserForm(forms.ModelForm):

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
