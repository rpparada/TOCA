from django.urls import path
from . import views

urlpatterns = [
    path('micarro', views.micarro, name='micarro'),
]
