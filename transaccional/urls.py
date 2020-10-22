from django.urls import path
from . import views

urlpatterns = [
    # Vistas de los correos
    path('tocatacancelada', views.TocataCanceladaView.as_view(), name='tocatacancelada'),
]
