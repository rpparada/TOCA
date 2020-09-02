from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from toca.parametros import parToca, parTocatas, parLugaresToc

User = settings.AUTH_USER_MODEL

# Create your models here.
class FacturacionProfileManager(models.Manager):

    def new_or_get(self, request):
        user = request.user
        created = False
        obj = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(usuario=user, email=user.email)
        else:
            pass

        return obj, created

class FacturacionProfile(models.Model):

    usuario             = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email               = models.EmailField()
    activo              = models.BooleanField(default=True)

    estado              = models.CharField(max_length=2, choices=parTocatas['estado_tipos'],default=parToca['publicado'])
    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    objects             = FacturacionProfileManager()

    def __str__(self):
        return self.email

def usuario_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        FacturacionProfile.objects.get_or_create(usuario=instance, email=instance.email)

post_save.connect(usuario_created_receiver, sender=User)
