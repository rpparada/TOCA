from django.urls import path
from . import views

urlpatterns = [
    path('ingresar', views.ingresar, name='ingresar'),
    path('registrar', views.registrar, name='registrar'),
    path('registrarart', views.registrarArt, name='registrarart'),
    path('cuenta', views.cuenta, name='cuenta'),
    path('salir', views.salir, name='salir'),
    path('actualizar', views.actualizar, name='actualizar'),
    path('cambiocontra', views.cambioContra, name='cambiocontra'),
    path('cuentaart', views.cuentaArt, name='cuentaart'),
    path('emailnuevacontra', views.emailNuevaContra, name='emailnuevacontra'),
    path('cambiocontra', views.cambioContra, name='cambiocontra'),
]
