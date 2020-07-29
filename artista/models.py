from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import pre_save

from django_resized import ResizedImageField

from toca.parametros import parToca, parArtistas
from tocata.utils  import unique_slug_generator

# Create your models here.
class Artista(models.Model):

    nombre              = models.CharField(max_length=200)
    slug                = models.SlugField(unique=True)
    usuario             = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    foto_1920_1280      = models.ImageField(upload_to='fotos/artistas/%Y/%m/%d/', blank=True)
    foto_525_350        = ResizedImageField(size=[525, 350],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'])
    foto_380_507        = ResizedImageField(size=[525, 350],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'])
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

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return "/artistas/{slug}".format(slug=self.slug)

def artista_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(artista_pre_save_receiver, sender=Artista)

class Estilo(models.Model):

    nombre              = models.CharField(max_length=200)
    slug                = models.SlugField(unique=True)
    activo              = models.BooleanField(default=True)

    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

def estilo_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(estilo_pre_save_receiver, sender=Estilo)

class Cualidad(models.Model):

    nombre              = models.CharField(max_length=200)
    slug                = models.SlugField(unique=True)
    activo              = models.BooleanField(default=True)

    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

def cualidad_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(cualidad_pre_save_receiver, sender=Cualidad)
