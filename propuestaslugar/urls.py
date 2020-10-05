from django.urls import path
from . import views

urlpatterns = [
    path('mispropuestas',views.MisPropuestasListView.as_view(), name='mispropuestas'),
    path('cancelarpropuesta',views.CancelarPropuestaView.as_view(), name='cancelarpropuesta'),
    path('borrarpropuesta',views.BorrarPropuestaView.as_view(), name='borrarpropuesta'),
    path('cancelarpropuestaelegida',views.CancelarPropuestaElegidaView.as_view(), name='cancelarpropuestaelegida'),
    path('proponerlugar', views.ProponerLugarListView.as_view(), name='proponerlugar'),
    path('seleccionarlugar', views.SeleccionarLugarView.as_view(), name='seleccionarlugar'),
    path('agregaryseleccionarlugar', views.AgregarYSeleccionarLugar.as_view(), name='agregaryseleccionarlugar'),
    path('artista/propuestas', views.VerPropuestasLitsView.as_view(), name='verpropuestas'),
    path('artista/seleccionarpropuesta', views.SeleccionarPropuestasView.as_view(), name='seleccionarpropuesta'),
]
