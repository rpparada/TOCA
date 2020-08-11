from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_save
from django.db.models import Q

from django_resized import ResizedImageField

from artista.models import Artista, Estilo
from lugar.models import Lugar, Region, Comuna

from toca.parametros import parToca, parTocatas, parLugaresToc, parTocatasAbiertas
from toca.utils  import unique_slug_generator

User = settings.AUTH_USER_MODEL
# Create your models here.

# Tocatas
class TocataQuerySet(models.query.QuerySet):

    def disponible(self):
        return self.filter(estado__in=[parToca['publicado'],parToca['confirmado'],])

    def busqueda(self, consulta):
        lookups = (Q(nombre__icontains=consulta) |
                    Q(descripción__icontains=consulta) |
                    Q(artista__nombre__icontains=consulta) |
                    Q(estilos__nombre__icontains=consulta)
                    )
        return self.filter(lookups).distinct()

    def tocataartista(self, artista):
        return self.filter(artista=artista)

class TocataManager(models.Manager):

    def get_queryset(self):
        return TocataQuerySet(self.model, using=self._db)

    def disponible(self):
        return self.get_queryset().disponible()

    def busqueda(self, consulta):
        return self.get_queryset().disponible().busqueda(consulta)

    def tocataartistadisponibles(self, artista):
        qs = self.get_queryset().disponible().tocataartista(artista)
        if qs:
            return qs
        return None

class Tocata(models.Model):

    artista             = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)
    usuario             = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nombre              = models.CharField(max_length=200)
    slug                = models.SlugField(blank=True, unique=True)
    lugar               = models.ForeignKey(Lugar, on_delete=models.DO_NOTHING, null=True, blank=True)
    region              = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True, blank=True)
    comuna              = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING, null=True, blank=True)
    descripción         = models.TextField(blank=True)
    costo               = models.DecimalField(max_digits=10,decimal_places=2)
    fecha               = models.DateField()
    hora                = models.TimeField()
    asistentes_total    = models.IntegerField(default=0)
    asistentes_min      = models.IntegerField()
    asistentes_max      = models.IntegerField()
    flayer_original     = models.ImageField(upload_to='fotos/tocatas/%Y/%m/%d/', blank=True, default='fotos/defecto/imagen_original.jpg')
    flayer_1920_1280    = ResizedImageField(size=[1920, 1280],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_1920_1280.jpg')
    flayer_380_507      = ResizedImageField(size=[380, 507],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_380_507.jpg')
    evaluacion          = models.IntegerField(choices=parToca['valoresEvaluacion'],default=parToca['defaultEvaluacion'])
    estilos             = models.ManyToManyField(Estilo, blank=True)
    estado              = models.CharField(max_length=2, choices=parTocatas['estado_tipos'],default=parToca['publicado'])

    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    objects             = TocataManager()

    def get_absolute_url(self):
        return "/tocatas/{slug}".format(slug=self.slug)

    def __str__(self):
        return str(self.id)+' '+self.nombre

def tocata_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tocata_pre_save_receiver, sender=Tocata)


# Tocatas Abiertas
class TocataAbiertaQuerySet(models.query.QuerySet):

    def disponible(self):
        return self.filter(estado__in=[parToca['publicado'],])

    def busqueda(self, consulta):
        lookups = (Q(nombre__icontains=consulta) |
                    Q(descripción__icontains=consulta) |
                    Q(artista__nombre__icontains=consulta) |
                    Q(estilos__nombre__icontains=consulta)
                    )
        return self.filter(lookups).distinct()

class TocataAbiertaManager(models.Manager):

    def get_queryset(self):
        return TocataAbiertaQuerySet(self.model, using=self._db)

    def disponible(self):
        return self.get_queryset().disponible()

    def busqueda(self, consulta):
        return self.get_queryset().disponible().busqueda(consulta)

class TocataAbierta(models.Model):

    artista             = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)
    usuario             = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nombre              = models.CharField(max_length=200)
    slug                = models.SlugField(blank=True, unique=True)
    region              = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True, blank=True)
    comuna              = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING, null=True, blank=True)
    descripción         = models.TextField(blank=True, null=True)
    costo               = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    fecha               = models.DateField()
    hora                = models.TimeField()
    asistentes_min      = models.IntegerField()
    flayer_original     = models.ImageField(upload_to='fotos/tocatas/%Y/%m/%d/', blank=True, default='fotos/defecto/imagen_original.jpg')
    flayer_1920_1280    = ResizedImageField(size=[1920, 1280],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_1920_1280.jpg')
    flayer_380_507      = ResizedImageField(size=[380, 507],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_380_507.jpg')
    tocata              = models.ForeignKey(Tocata, on_delete=models.DO_NOTHING, null=True, blank=True)
    estilos             = models.ManyToManyField(Estilo, blank=True)
    estado              = models.CharField(max_length=2, choices=parTocatasAbiertas['estado_tipos'],default=parToca['publicado'])

    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    objects             = TocataAbiertaManager()

    def get_absolute_url(self):
        return "/tocatas/tocataabierta/{slug}".format(slug=self.slug)

    def __str__(self):
        return self.nombre

def tocataabierta_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tocataabierta_pre_save_receiver, sender=TocataAbierta)

# Lugares Tocata
class LugaresTocata(models.Model):

    tocataabierta       = models.ForeignKey(TocataAbierta, on_delete=models.DO_NOTHING)
    lugar               = models.ForeignKey(Lugar, on_delete=models.DO_NOTHING)
    estado              = models.CharField(max_length=2, choices=parLugaresToc['estado_lugartocata'],default=parToca['pendiente'])

    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tocataabierta.nombre+' - '+str(self.lugar.nombre_calle)+' '+str(self.lugar.numero)
