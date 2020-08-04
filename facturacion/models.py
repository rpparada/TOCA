from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from toca.parametros import parToca, parTocatas, parLugaresToc, parTocatasAbiertas

# Create your models here.
class FacturacionProfile(models.Model):

    usuario             = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email               = models.EmailField()
    activo              = models.BooleanField(default=True)

    estado              = models.CharField(max_length=2, choices=parTocatas['estado_tipos'],default=parToca['publicado'])
    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

def usuario_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        FacturacionProfile.objects.get_or_create(usuario=instance, email=instance.email)

post_save.connect(usuario_created_receiver, sender=User)
