from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import (
            TocatasCanceladasListView,
            )

urlpatterns = [
    path('', TocatasCanceladasListView.as_view(), name='cancelaciones'),
]
