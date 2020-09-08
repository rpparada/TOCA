from django.contrib import admin
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import EmailActivation

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

# Register your models here.
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin','musico')
    list_filter = ('admin','staff','is_active','musico')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nombre','apellido',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active','musico')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','nombre','apellido',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)


class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model = EmailActivation

admin.site.register(EmailActivation, EmailActivationAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
