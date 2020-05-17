from django.urls import path
from . import views

urlpatterns = [
    path('', views.tocatas, name='tocatas'),
    path('<int:tocata_id>', views.tocata, name='tocata'),
    path('proponerlugar_<int:tocata_id>', views.proponerlugar, name='proponerlugar'),
    path('artista/mistocatas', views.mistocatas, name='mistocatas'),
    path('artista/creartocata', views.creartocata, name='creartocata'),
    path('artista/borrartocata_<int:tocata_id>', views.borrartocata, name='borrartocata'),
    path('artista/suspendertocata_<int:tocata_id>', views.suspendertocata, name='suspendertocata'),
    path('artista/propuestas_<int:tocata_id>', views.seleccionarPropuestas, name='propuestas'),
    path('ajax/load-comunas_tocata/', views.carga_comunas_tocata, name='ajax_load_comunas_tocata'),
]
