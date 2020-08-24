from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import OrdenCompraListView, OrdenCompraDetailView

urlpatterns = [
    path('', OrdenCompraListView.as_view(), name='list'),
    path('<int:orden_id>/', OrdenCompraDetailView.as_view(), name='detail'),
]
