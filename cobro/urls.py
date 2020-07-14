from django.urls import path
from . import views

urlpatterns = [
    path('micarro', views.micarro, name='micarro'),
    path('agregaracarro_<int:tocata_id>', views.agregaracarro, name='agregaracarro'),
    path('quitarcarro_<int:item_id>', views.quitarcarro, name='quitarcarro'),

    path('prueba', views.prueba, name='prueba'),
    path('iniciar', views.iniciar, name='iniciar'),
    path('volver', views.volver, name='volver'),
    path('final', views.final, name='final')

]
