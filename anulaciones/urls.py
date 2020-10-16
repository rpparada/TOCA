from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import (
            TocatasCanceladasListView,
            EntradasTocataCanceladaListView,
            MarcarComoEnviadaTBKView,
            MarcarComoReembolsadoView,
            MarcarComoReembolsadoTBKView
            )

urlpatterns = [
    path('', TocatasCanceladasListView.as_view(), name='cancelaciones'),
    path('entradas/<slug:slug>', EntradasTocataCanceladaListView.as_view(), name='anulacion'),
    path('enviartbk/<slug:slug>', MarcarComoEnviadaTBKView.as_view(), name='enviartbk'),
    path('reembolsado/<slug:slug>', MarcarComoReembolsadoView.as_view(), name='reembolsado'),
    path('reembolsadotbk/<slug:slug>', MarcarComoReembolsadoTBKView.as_view(), name='reembolsadotbk'),
]
