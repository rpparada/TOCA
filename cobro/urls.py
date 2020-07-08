from django.urls import path
from . import views

urlpatterns = [
    path('micarro', views.micarro, name='micarro'),
    path('agregaracarro_<int:tocata_id>', views.agregaracarro, name='agregaracarro'),
    path('quitarcarro_<int:item_id>', views.quitarcarro, name='quitarcarro'),
]
