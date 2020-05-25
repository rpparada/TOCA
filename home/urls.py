from django.urls import path
from . import views

urlspatterns = [
    path('', views.index, name='index'),
    path('busqueda', views.busqueda, name='busqueda'),
]
