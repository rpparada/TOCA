from django.urls import path
from . import views

urlpatterns = [
    #path('', views.artistas, name='artistas'),
    path('', views.ArtistasListView.as_view(), name='artistas'),
    path('<slug:slug>/', views.ArtistaDetailView.as_view(), name='artista'),
]
