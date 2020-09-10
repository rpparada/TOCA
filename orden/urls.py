from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import OrdenCompraListView, OrdenCompraDetailView, ITicketDownloadView

urlpatterns = [
    path('', OrdenCompraListView.as_view(), name='listacompras'),
    path('<str:orden_id>/', OrdenCompraDetailView.as_view(), name='detailcompra'),
    path('<int:orden_id>/<int:pk>/', ITicketDownloadView.as_view(), name='downloadticket'),
]
