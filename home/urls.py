from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('busqueda', views.busqueda, name='busqueda'),
]
