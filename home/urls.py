from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busqueda', views.busqueda, name='busqueda'),
    path('busqueda_test', views.busqueda_test, name='busqueda_test'),
]
