from django.urls import path
from . import views

urlpatterns = [
    path('', views.carro_home, name='carro'),
    path('actualizarcarro/', views.carro_actualizar, name='actualizarcarro')
]
