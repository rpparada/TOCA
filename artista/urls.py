from django.urls import path
from . import views

urlpatterns = [
    path('', views.artistas, name='artistas'),
    path('<int:artista_id>', views.artista, name='artista'),
]
