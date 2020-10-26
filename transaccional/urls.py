from django.urls import path
from . import views

urlpatterns = [
    # Vistas de los correos
    path('tocatacancelada', views.TocataCanceladaView.as_view(), name='tocatacancelada'),
    path('tocatacanceladaartista', views.TocataCanceladaArtistaView.as_view(), name='tocatacanceladaartista'),
    path('recuperarpassword', views.RecuperarPasswordView.as_view(), name='recuperarpassword'),
    path('validacionemail', views.ValidacionEmailView.as_view(), name='validacionemail'),
    path('formularionuevoartista', views.FormularioNuevoArtistaView.as_view(), name='formularionuevoartista'),
    path('bienvenidonuevousuario', views.BienvenidoNuevoUsuarioView.as_view(), name='bienvenidonuevousuario'),
    path('bienvenidonuevoartista', views.BienvenidoNuevoArtistaView.as_view(), name='bienvenidonuevoartista')
]
