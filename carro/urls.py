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

    #path('checkout/fin', views.checkout_complete_view, name='checkout_complete'),
    path('api/carro', views.carro_detalle_api_body_view, name='api-carro'),

    # Prueba Render to PDF
    path('pdf/', views.GeneraPDF.as_view(), name='pdf')

]
