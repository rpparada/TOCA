from django.urls import path
from . import views

urlpatterns = [
    path('mispropuestas',views.MisPropuestasListView.as_view(), name='mispropuestas'),
    path('cancelarpropuesta',views.CancelarPropuestaView.as_view(), name='cancelarpropuesta'),
    path('borrarpropuesta',views.BorrarPropuestaView.as_view(), name='borrarpropuesta'),
    path('cancelarpropuestaelegida',views.CancelarPropuestaElegidaView.as_view(), name='cancelarpropuestaelegida'),
    path('proponerlugar', views.ProponerLugarView.as_view(), name='proponerlugar'),
    path('artista/propuestas', views.VerPropuestasLitsView.as_view(), name='verpropuestas'),
    #path('artista/propuestas_<int:tocata_id>', views.verpropuestas, name='verpropuestas'),
    path('artista/seleccionarpropuestas_<int:tocata_id>_<int:lugar_id>', views.seleccionarpropuestas, name='seleccionarpropuestas'),

]
