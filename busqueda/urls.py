from django.urls import path
from . import views

urlpatterns = [
    path('', views.BusquedaTocataView.as_view(), name='busqueda_test'),
]
