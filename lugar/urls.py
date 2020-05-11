from django.urls import path
from . import views

urlpatterns = [
    path('mislugares',views.misLugares, name='mislugares'),
    path('agregarlugar', views.agregarLugar, name='agregarlugar'),
    path('<int:lugar_id>', views.detalleslugar, name='lugar'),
    path('borrar_<int:lugar_id>', views.borrarlugar, name='borrarlugar'),
    path('actualizar_<int:lugar_id>', views.atualizarLugar, name='atualizarlugar'),

    path('ajax/load-comunas_agregar/', views.carga_comunas_agregar, name='ajax_load_comunas_agregar'),
    path('ajax/load-comunas_actualizar/', views.carga_comunas_actualizar, name='ajax_load_comunas_actualizar'),
]
