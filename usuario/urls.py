from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('ingresar', views.ingresar, name='ingresar'),
    path('registrar', views.registrar, name='registrar'),
    path('registrarart', views.registrarArt, name='registrarart'),
    path('cuenta', views.cuenta, name='cuenta'),
    path('salir', views.salir, name='salir'),
    path('actualizar', views.actualizar, name='actualizar'),
    path('actualizarart', views.actualizarArt, name='actualizarart'),
    path('cambiocontra', views.cambioContra, name='cambiocontra'),
    path('cuentaart', views.cuentaArt, name='cuentaart'),
    path('cambiocontra', views.cambioContra, name='cambiocontra'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='usuario/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='usuario/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='usuario/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='usuario/password_reset_complete.html'), name='password_reset_complete'),
    path('formularionuevoartista', views.enviaform, name='enviaform'),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    re_path('activateart/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activateArt, name='activateart'),
]
