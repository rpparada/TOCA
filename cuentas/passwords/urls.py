# accounts.passwords.urls.py
# from django.conf.urls import url
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from cuentas.forms import CuentaPasswordChangeForm, CuentaPasswordResetForm, CuentaSetPasswordForm

urlpatterns  = [
    path('password/change/',
            auth_views.PasswordChangeView.as_view(form_class=CuentaPasswordChangeForm),
            name='password_change'),
    path('password/change/done/',
            auth_views.PasswordChangeDoneView.as_view(),
            name='password_change_done'),
    path('password/reset/',
            auth_views.PasswordResetView.as_view(
                    form_class=CuentaPasswordResetForm,
                    html_email_template_name='registration/html_password_reset_email.html'
                    ),
            name='password_reset'),
    path('password/reset/done/',
            auth_views.PasswordResetDoneView.as_view(),
            name='password_reset_done'),
    re_path('password/reset/\
            (?P<uidb64>[0-9A-Za-z_\-]+)/\
            (?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(form_class=CuentaSetPasswordForm),
            name='password_reset_confirm'),
    path('password/reset/complete/',
            auth_views.PasswordResetCompleteView.as_view(),
            name='password_reset_complete'),
]
