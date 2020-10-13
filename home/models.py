from django.db import models
from django.db.models.signals import pre_save

from artista.models import Artista

from toca.utils  import unique_slug_generator

# Create your models here.
# Testimonios
class TestimonioQuerySet(models.QuerySet):
    def para_artistas(self):
        return self.filter(objetivo='artistas')

    def para_usuarios(self):
        return self.filter(objetivo='usuarios')

class TestimonioManager(models.Manager):
    def get_queryset(self):
        return TestimonioQuerySet(self.model, using=self._db)

    def get_testimonio_by_request(self, request):
        if request.user.is_musico:
            return self.get_queryset().para_artistas().order_by('fecha_crea')
        return self.get_queryset().para_usuarios().order_by('fecha_crea')

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
    testimonio          = models.CharField(max_length=120, blank=True)
    objetivo            = models.CharField(max_length=20, choices=TESTIMONIO_OBJETIVO_OPCIONES,default='usuarios')

    estado              = models.CharField(max_length=20, choices=TESTIMONIO_ESTADO_OPCIONES,default='disponible')
    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    objects             = TestimonioManager()

    def __str__(self):
        return str(self.artista)+'('+str(self.objetivo)+'): '+str(self.testimonio[:100])

# Descripcion TocatasIntimas
class DescripcionTocatasIntimasQuerySet(models.QuerySet):
    def para_artistas(self):
        return self.filter(objetivo='artistas')

    def para_usuarios(self):
        return self.filter(objetivo='usuarios')

class DescripcionTocatasIntimasManager(models.Manager):
    def get_queryset(self):
        return DescripcionTocatasIntimasQuerySet(self.model, using=self._db)

    def get_descripcion_by_request(self, request):
        if request.user.is_musico:
            return self.get_queryset().para_artistas().order_by('fecha_crea')

        return self.get_queryset().para_usuarios().order_by('fecha_crea')

DESCRIPCION_OBJETIVO_OPCIONES = (
    ('artistas','Artistas'),
    ('usuarios','Usuarios'),
)

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
