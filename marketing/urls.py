from django.urls import path
from . import views

urlpatterns = [
    path('conf/email', views.MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
]
