from django.urls import path
from . import views

urlpatterns = [
    path('checkout/create', views.checkout_direccion_create_view, name='checkout_direccion_create_view'),
]
