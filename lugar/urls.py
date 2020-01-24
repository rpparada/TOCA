from django.urls import path
from . import views

urlpatterns = [
    path('lugar/agregar', views.agregar, name='agregar'),
    path('lugar/detalles/<int:lugar_id>', views.detalleslugar, name='detalleslugar'),
    path('lugar/<int:lugar_id>', views.borrarlugar, name='borrarlugar'),
    path('lugar/editar/<int:lugar_id>', views.editarlugar, name='editarlugar'),
]
