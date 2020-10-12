from django.urls import path
from . import views

urlpatterns = [
    # Vistas Generales
    path('', views.TocataListView.as_view(), name='tocatas'),
    path('<slug:slug>/', views.TocataDetailView.as_view(), name='tocata'),
    path('artista/mistocatas', views.TocatasArtistaListView.as_view(), name='mistocatas'),
    path('artista/creartocata', views.TocataCreateView.as_view(), name='creartocata'),
    path('artista/seleccionardireccion_<slug:slug>', views.SeleccionarLugarTocataView.as_view(), name='seleccionardireccion'),
    path('artista/creartocatadesdetocataabierta', views.TocataDesdeTocataAbiertaCreateView.as_view(), name='creartocatadesdetocataabierta'),
    path('artista/borrartocata', views.BorrarTocataView.as_view(), name='borrartocata'),
    path('artista/suspendertocata', views.SuspenderTocataView.as_view(), name='suspendertocata'),
]
