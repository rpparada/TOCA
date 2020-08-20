from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.CuentaHomeView.as_view(), name='cuenta'),
    path('ingresar', views.IngresarView.as_view(), name='ingresar'),
    path('registrar', views.RegistrarView.as_view(), name='registrar'),
    path('salir', auth_views.LogoutView.as_view(), name='salir'),
    re_path('email/confirm/(?P<key>[0-9A-Za-z]+)/$', views.CuentaEmailActivacionView.as_view(), name='email-activate'),
    path('email/resent-activation/', views.CuentaEmailActivacionView.as_view(), name='resent-activation'),
    path('email/confirm/done', views.RegistrarDoneView.as_view(), name='registrar-done'),

]
