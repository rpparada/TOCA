from django.urls import path
from . import views

urlpatterns = [
    path('', views.tocatas, name='tocatas'),
    path('<int:tocata_id>', views.tocata, name='tocata'),
    path('pago',views.mediopago, name='pago')
]
