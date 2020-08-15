"""toca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('home.urls')),
    path('artistas/', include('artista.urls')),
    path('lugares/', include('lugar.urls')),
    path('tocatas/', include('tocata.urls')),
    path('tocatasabiertas/', include('tocataabierta.urls')),
    path('usuarios/', include('usuario.urls')),
    path('cuentas/', include('cuentas.urls')),
    path('cobro/', include('cobro.urls')),
    path('busqueda/', include('busqueda.urls')),
    path('carro/', include('carro.urls')),
    path('direccion/', include('direccion.urls')),
    path('admin/', admin.site.urls),
    #path('carro/', views.carro_home, name='carro')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
