from django.urls import path
from . import views

urlpatterns = [
    path('', views.carro_home, name='carro'),
    path('actualizarcarro/', views.carro_actualizar, name='actualizarcarro'),
    path('checkout/', views.checkout_home, name='checkout'),
    path('checkout/fin', views.checkout_complete_view, name='checkout_complete'),
    path('ajaxdir/load-comunas_agregar/', views.carga_comunas_agregar, name='ajax_load_comunas_agregar_test'),
    path('ajaxdir/load-comunas_actualizar/', views.carga_comunas_actualizar, name='ajax_load_comunas_actualizar_test'),
]
