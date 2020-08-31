from django.urls import path
from . import views

urlpatterns = [
    path('', views.carro_home, name='carro'),
    path('actualizarcarro/', views.carro_actualizar, name='actualizarcarro'),
    path('actualizarcarro/suma/', views.carro_actualizar_suma, name='actualizarcarrosuma'),
    path('actualizarcarro/resta/', views.carro_actualizar_resta, name='actualizarcarroresta'),
    path('checkout/', views.checkout_home, name='checkout'),
    
    path('retornotbk', views.retornotbk, name='retornotbk'),
    path('compraexitosa', views.compraexitosa, name='compraexitosa'),
    path('fincompra', views.fincompra, name='fincompra'),
    path('finerrorcompra', views.finerrorcompra, name='finerrorcompra'),

    path('checkout/fin', views.checkout_complete_view, name='checkout_complete'),
    #path('api/carro', views.carro_detalle_api_view, name='api-carro'),
    path('api/carro', views.carro_detalle_api_body_view, name='api-carro'),
    path('ajaxdir/load-comunas_agregar/', views.carga_comunas_agregar, name='ajax_load_comunas_agregar_test'),
    path('ajaxdir/load-comunas_actualizar/', views.carga_comunas_actualizar, name='ajax_load_comunas_actualizar_test'),
]
