# cuentas.forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordChangeForm

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
                                                                "placeholder": "Email"
                                                            }), label=''
                                    )
    contra          = forms.CharField(widget=forms.PasswordInput(attrs={
                                                                "id": "contra",
                                                                "class": "form-control",
                                                                "placeholder": "Contraseña"
                                                            }), label=''
                                    )

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
        #user.active = False
        # Aqui va el checkeo email
        if commit:
            user.save()
        return user

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
