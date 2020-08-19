from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.CuentaHomeView.as_view(), name='cuenta'),
    path('ingresar', views.IngresarView.as_view(), name='ingresar'),
    path('registrar', views.RegistrarView.as_view(), name='registrar'),
]
