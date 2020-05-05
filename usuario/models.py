from django.db import models
from django.contrib.auth.models import User

from artista.models import Artista

from toca.parametros import parUsuarioArtistas, parToca

# Create your models here.
class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    es_artista = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class UsuarioArtista(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    rut = models.IntegerField(default=0)
    num_celular = models.CharField(max_length=50, default=0)
    digitoVerificador = models.CharField(max_length=1,default='0')
    banco = models.CharField(max_length=200, choices=parUsuarioArtistas['bancos'],default=parToca['bancoDefecto'])
    num_cuenta = models.CharField(max_length=100,default='0')
    tipo_cuenta = models.CharField(max_length=200, choices=parUsuarioArtistas['tipo_cuenta'],default=parToca['tipoCuentaDefecto'])
    artista = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username
