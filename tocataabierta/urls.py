from django.urls import path
from . import views

urlpatterns = [
    #path('', views.TocataListView.as_view(), name='tocatas'),
    #path('<slug:slug>/', views.TocataDetailView.as_view(), name='tocata'),
    path('<slug:slug>/', views.TocataAbiertaDetailView.as_view(), name='tocataabierta'),
    #path('proponerlugar_<int:tocata_id>', views.proponerlugar, name='proponerlugar'),
    #path('artista/mistocatas', views.mistocatas, name='mistocatas'),
    #path('artista/creartocatacerrada', views.creartocatacerrada, name='creartocatacerrada'),
    path('artista/creartocataabierta', views.creartocataabierta, name='creartocataabierta'),
    path('artista/detallestocataabierta_<int:tocata_id>', views.detallestocataabierta, name='detallestocataabierta'),
    #path('artista/detallestocata_<int:tocata_id>', views.detallestocata, name='detallestocata'),
    #path('artista/creartocata', views.creartocata, name='creartocata'),
    #path('artista/borrartocata_<int:tocata_id>', views.borrartocata, name='borrartocata'),
    path('artista/borrartocataabierta_<int:tocata_id>', views.borrartocataabierta, name='borrartocataabierta'),
    #path('artista/suspendertocata_<int:tocata_id>', views.suspendertocata, name='suspendertocata'),
    path('artista/suspendertocataabierta_<int:tocata_id>', views.suspendertocataabierta, name='suspendertocataabierta'),
    #path('artista/propuestas_<int:tocata_id>', views.verpropuestas, name='verpropuestas'),
    #path('artista/seleccionarpropuestas_<int:tocata_id>_<int:lugar_id>', views.seleccionarpropuestas, name='seleccionarpropuestas'),
    path('ajax/load-comunas_tocata/', views.carga_comunas_tocata, name='ajax_load_comunas_tocata'),
]
