from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_save

from toca.parametros import parToca, parArtistas
from toca.utils  import unique_slug_generator

User = settings.AUTH_USER_MODEL
# Create your models here.

# Artistas
class ArtistaQuerySet(models.query.QuerySet):
    def disponible(self):
        return self.filter(estado=parToca['disponible'])

class ArtistaManager(models.Manager):

    def get_queryset(self):
        return ArtistaQuerySet(self.model, using=self._db)

    def disponible(self):
        qs = self.get_queryset().disponible()
        if qs:
            return qs
        return None

    def get_artistas_destacados(self, num_muestra):
        # Por ahora el criterio de mejores tocatas solo contemplara la fecha de creacion
        qs = self.get_queryset().disponible().order_by('-fecha_crea')[:num_muestra]
        if qs:
            return qs
        return None

def upload_fotos_artista_loc(instance, filename):
    slug = instance.slug
    if not slug:
        slug = unique_slug_generator(instance)

    location = 'fotos/artistas/{}/'.format(slug)
    return location + filename

class Artista(models.Model):

    nombre              = models.CharField(max_length=200)
    slug                = models.SlugField(blank=True, unique=True)
    usuario             = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    foto_1920_1280      = models.ImageField(upload_to=upload_fotos_artista_loc, blank=True)
    foto_525_350        = models.ImageField(upload_to=upload_fotos_artista_loc, blank=True)
    foto_380_507        = models.ImageField(upload_to=upload_fotos_artista_loc, blank=True)
    descripción         = models.TextField(blank=True)
    cualidades          = models.ManyToManyField('Cualidad', blank=True)
    estilos             = models.ManyToManyField('Estilo', blank=True)
    email               = models.EmailField(max_length=254, blank=True)
    telefono_contacto   = models.CharField(max_length=200, blank=True)
    link_facebook       = models.URLField(max_length=200, blank=True)
    link_twitter        = models.URLField(max_length=200, blank=True)
    link_instagram      = models.URLField(max_length=200, blank=True)

    estado              = models.CharField(max_length=2, choices=parArtistas['estado_tipos'],default=parToca['disponible'])
    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    objects             = ArtistaManager()

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return "/artistas/{slug}".format(slug=self.slug)

def artista_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(artista_pre_save_receiver, sender=Artista)

# Estilo
class EstiloQuerySet(models.query.QuerySet):
    def activo(self):
        return self.filter(activo=True)

class EstiloManager(models.Manager):

    def get_queryset(self):
        return EstiloQuerySet(self.model, using=self._db)

    def activo(self):
        qs = self.get_queryset().activo()
        if qs:
            return qs
        return None

class Estilo(models.Model):

    nombre              = models.CharField(max_length=200)
    slug                = models.SlugField(blank=True, unique=True)
    activo              = models.BooleanField(default=True)

    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    objects             = EstiloManager()

    def __str__(self):
        return self.nombre

def estilo_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(estilo_pre_save_receiver, sender=Estilo)

# Cualidad
class Cualidad(models.Model):

    nombre              = models.CharField(max_length=200)
    slug                = models.SlugField(blank=True, unique=True)
    activo              = models.BooleanField(default=True)

    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

def cualidad_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(cualidad_pre_save_receiver, sender=Cualidad)
