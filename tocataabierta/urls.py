from django.urls import path
from . import views

urlpatterns = [
    path('', views.TocataAbiertaListView.as_view(), name='tocatasabiertas'),
    path('<slug:slug>/', views.TocataAbiertaDetailView.as_view(), name='tocataabierta'),
    path('artista/mistocatasabiertas', views.TocatasAbiertasArtistaListView.as_view(), name='mistocatasabiertas'),
    path('artista/creartocataabierta', views.TocataAbiertaCreateView.as_view(), name='creartocataabierta'),
    path('artista/borrartocataabierta', views.BorrarTocataAbiertaView.as_view(), name='borrartocataabierta'),
    path('artista/suspendertocataabierta', views.SuspenderTocataAbiertaView.as_view(), name='suspendertocataabierta'),
    path('ajax/load-comunas_tocata/', views.carga_comunas_tocata, name='ajax_load_comunas_tocata'),
]
