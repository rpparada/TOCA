from django.urls import path
from . import views

urlpatterns = [
    path('micarro', views.micarro, name='micarro'),
    path('agregaracarro_<int:tocata_id>', views.agregaracarro, name='agregaracarro'),
    path('quitarcarro_<int:item_id>', views.quitarcarro, name='quitarcarro'),
    path('comprar', views.comprar, name='comprar'),
    path('procesarorden_<int:orden_id>', views.procesarorden, name='procesarorden'),
    path('retornotbk', views.retornotbk, name='retornotbk'),
    path('compraexitosa', views.compraexitosa, name='compraexitosa')

]
