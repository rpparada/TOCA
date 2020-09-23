from django.urls import path
from . import views

urlpatterns = [
    # Vistas Generales
    path('', views.TocataListView.as_view(), name='tocatas'),
    path('<slug:slug>/', views.TocataDetailView.as_view(), name='tocata'),
    # Vistas Artista
    path('artista/mistocatas', views.TocatasArtistaListView.as_view(), name='mistocatas'),
    path('artista/creartocata', views.CrearTocataView.as_view(), name='creartocata'),
    #path('artista/creartocata', views.creartocatacerrada, name='creartocata'),
    path('artista/borrartocata', views.BorrarTocataView.as_view(), name='borrartocata'),
    path('artista/suspendertocata', views.SuspenderTocataView.as_view(), name='suspendertocata'),
    path('ajax/load-comunas_tocata/', views.carga_comunas_tocata, name='ajax_load_comunas_tocata'),
]
