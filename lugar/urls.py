from django.urls import path
from . import views

urlpatterns = [
    path('mislugares',views.MisLugaresListView.as_view(), name='mislugares'),
    path('mispropuestas',views.mispropuestas, name='mispropuestas'),
    path('cancelarpropuesta_<int:propuesta_id>',views.cancelarpropuesta, name='cancelarpropuesta'),
    path('cancelarpropuestaelegida_<int:propuesta_id>',views.cancelarpropuestaelegida, name='cancelarpropuestaelegida'),
    path('borrarpropuesta_<int:propuesta_id>',views.borrarpropuesta, name='borrarpropuesta'),
    path('agregarlugar', views.LugarCreateView.as_view(), name='agregarlugar'),
    path('actualizarlugar', views.ActualizaLugarView.as_view(), name='actualizarlugar'),
    path('borrar', views.BorrarLugarView.as_view(), name='borrarlugar'),
    path('ajax/load-comunas_agregar/', views.carga_comunas_agregar, name='ajax_load_comunas_agregar'),
    path('ajax/load-comunas_actualizar/', views.carga_comunas_actualizar, name='ajax_load_comunas_actualizar'),
]
