from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    #path('', views.index, name='index'),
]
