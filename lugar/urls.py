from django.urls import path
from . import views

urlpatterns = [
    path('mislugares',views.misLugares, name='mislugares'),
    path('mispropuestas',views.mispropuestas, name='mispropuestas'),
    path('cancelarpropuesta_<int:propuesta_id>',views.cancelarpropuesta, name='cancelarpropuesta'),
    path('borrarpropuesta_<int:propuesta_id>',views.borrarpropuesta, name='borrarpropuesta'),
    path('agregarlugar', views.agregarLugar, name='agregarlugar'),
    path('actualizarlugar_<int:lugar_id>', views.actualizarLugar, name='actualizarlugar'),
    path('borrar_<int:lugar_id>', views.borrarlugar, name='borrarlugar'),
    path('ajax/load-comunas_agregar/', views.carga_comunas_agregar, name='ajax_load_comunas_agregar'),
    path('ajax/load-comunas_actualizar/', views.carga_comunas_actualizar, name='ajax_load_comunas_actualizar'),
]
