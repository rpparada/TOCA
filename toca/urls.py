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
from django.views.generic import RedirectView

urlpatterns = [
    path('', include('home.urls')),
    path('artistas/', include('artista.urls')),
    path('lugares/', include(('lugar.urls','lugar'), namespace='lugar')),
    path('tocatas/', include(('tocata.urls','tocata'), namespace='tocata')),
    path('ofrecetucasa/', include(('tocataabierta.urls','tocataabierta'), namespace='tocataabierta')),
    path('propuestaslugar/', include(('propuestaslugar.urls','propuestaslugar'), namespace='propuestaslugar')),
    path('cuentas/', RedirectView.as_view(url='/cuenta/')),
    path('cuentas/', include('cuentas.passwords.urls')),
    path('cuenta/', include(('cuentas.urls','cuentas'), namespace='cuenta')),
    path('busqueda/', include(('busqueda.urls','busqueda'), namespace='busqueda')),
    path('ordenes/', include(('orden.urls','ordenes'), namespace='ordenes')),
    path('cancelaciones/', include(('anulaciones.urls','cancelaciones'), namespace='cancelaciones')),
    path('carro/', include(('carro.urls','carro'), namespace='carro')),
    path('marketing/', include(('marketing.urls','marketing'), namespace='marketing')),
    # Temporal mientras revisamos el formato del correo
    path('transaccional/', include(('transaccional.urls','transaccional'), namespace='transaccional')),
    path('direccion/', include('direccion.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
