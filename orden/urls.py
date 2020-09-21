from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import (
            OrdenCompraListView,
            OrdenCompraDetailView,
            OrdenDownloadView,
            EntradasComprasDetailView,
            EntradasComprasListView,
            ITicketDownloadView,
            )

urlpatterns = [
    path('ordenes', OrdenCompraListView.as_view(), name='ordenes'),
    path('entradas', EntradasComprasListView.as_view(), name='entradas'),

    path('<str:orden_id>/', OrdenCompraDetailView.as_view(), name='detalleorden'),
    path('<str:orden_id>/<int:pk>/', EntradasComprasDetailView.as_view(), name='detalleentrada'),

    path('<str:orden_id>/download/', OrdenDownloadView.as_view(), name='downloadorden'),
    path('<str:orden_id>/<int:pk>/download/', ITicketDownloadView.as_view(), name='downloadticket'),
]
