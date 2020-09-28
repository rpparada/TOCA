from django.urls import path
from . import views

urlpatterns = [
    path('mispropuestas',views.MisPropuestasListView.as_view(), name='mispropuestas'),
    #path('mispropuestas',views.mispropuestas, name='mispropuestas'),
    path('cancelarpropuesta_<int:propuesta_id>',views.cancelarpropuesta, name='cancelarpropuesta'),
    path('cancelarpropuestaelegida_<int:propuesta_id>',views.cancelarpropuestaelegida, name='cancelarpropuestaelegida'),
    path('borrarpropuesta_<int:propuesta_id>',views.borrarpropuesta, name='borrarpropuesta'),
    path('proponerlugar_<int:tocata_id>', views.proponerlugar, name='proponerlugar'),
    path('artista/propuestas_<int:tocata_id>', views.verpropuestas, name='verpropuestas'),
    path('artista/seleccionarpropuestas_<int:tocata_id>_<int:lugar_id>', views.seleccionarpropuestas, name='seleccionarpropuestas'),

]
