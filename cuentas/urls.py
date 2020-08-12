from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('ingresar', views.ingresar, name='ingresar'),
]
