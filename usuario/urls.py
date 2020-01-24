from django.urls import path
from . import views

urlpatterns = [
    path('ingresar', views.ingresar, name='ingresar'),
    path('registrar', views.registrar, name='registrar'),
    path('cuenta', views.cuenta, name='cuenta'),
    path('salir', views.salir, name='salir'),
    path('actualizar', views.actualizar, name='actualizar'),
]
