from django.db import models
from django.db.models.signals import pre_save

from artista.models import Artista

from toca.utils  import unique_slug_generator

# Create your models here.
# Testimonios
TESTIMONIO_ESTADO_OPCIONES = (
    ('disponible','Disponible'),
    ('nodisponible','No Disponible'),
)

TESTIMONIO_OBJETIVO_OPCIONES = (
    ('artistas','Artistas'),
    ('usuarios','Usuarios'),
)
class Testimonio(models.Model):

    artista             = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)
    slug                = models.SlugField(blank=True, unique=True)
    testimonio          = models.CharField(max_length=120, blank=True)
    objetivo            = models.CharField(max_length=20, choices=TESTIMONIO_OBJETIVO_OPCIONES,default='usuarios')

    estado              = models.CharField(max_length=20, choices=TESTIMONIO_ESTADO_OPCIONES,default='disponible')
    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.artista)+'('+str(self.objetivo)+'): '+str(self.testimonio[:100])

def testimonio_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(testimonio_pre_save_receiver, sender=Testimonio)

# Descripcion TocatasIntimas
DESCRIPCION_OBJETIVO_OPCIONES = (
    ('artistas','Artistas'),
    ('usuarios','Usuarios'),
)

class DescripcionTocatasIntimasQuerySet(models.QuerySet):
    def solo_artistas(self):
        return self.filter(objetivo='artistas')
    def solo_usuarios(self):
        return self.filter(objetivo='usuarios')
    def ordenar_fecha_crea(self):
        return self.order_by('fecha_crea')

class DescripcionTocatasIntimasManager(models.Manager):
    def get_queryset(self):
        return DescripcionTocatasIntimasQuerySet(self.model, using=self._db)

    def get_descripcion(self, request):
        tipo_usuario = request.session.get('es_artista', 'N')
        if tipo_usuario == 'S':
            return self.get_queryset().solo_artistas().ordenar_fecha_crea()

        return self.get_queryset().solo_usuarios().ordenar_fecha_crea()

class DescripcionTocatasIntimas(models.Model):

    titulo              = models.CharField(max_length=30)
    descripcion         = models.CharField(max_length=150)
    color               = models.CharField(max_length=7, default='#2F2F2F')
    icono               = models.CharField(max_length=50, default='fa fa-users')
    objetivo            = models.CharField(max_length=20, choices=DESCRIPCION_OBJETIVO_OPCIONES,default='usuarios')

    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    objects             = DescripcionTocatasIntimasManager()

    def __str__(self):
        return self.objetivo+' '+self.titulo
