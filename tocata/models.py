from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.urls import reverse

from django_resized import ResizedImageField

import os

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
        return self.none()

    def get_mejores_tocatas(self, num_muestra):
        # Por ahora el criterio de mejores tocatas solo contemplara la fecha de creacion
        qs = self.get_queryset().disponible().order_by('-fecha_crea')[:num_muestra]
        if qs:
            return qs
        return self.none()

def upload_tocata_flayer_file_loc(instance, filename):
    slug =instance.slug
    if not slug:
        slug = unique_slug_generator(instance)

    location = 'tocata/fotos/{}/'.format(slug)
    return location + filename

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
    flayer_original     = models.ImageField(upload_to=upload_tocata_flayer_file_loc, blank=True, default='fotos/defecto/imagen_original.jpg')
    flayer_1920_1280    = ResizedImageField(size=[1920, 1280],upload_to=upload_tocata_flayer_file_loc, blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_1920_1280.jpg')
    flayer_380_507      = ResizedImageField(size=[380, 507],upload_to=upload_tocata_flayer_file_loc, blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_380_507.jpg')
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

    @property
    def name(self):
        return self.name

    def get_downloads(self):
        qs = self.tocataticketfile_set.all()
        return qs

def tocata_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tocata_pre_save_receiver, sender=Tocata)

# Tocata ITicket
def upload_tocata_ticket_file_loc(instance, filename):
    slug =instance.tocata.slug
    if not slug:
        slug = unique_slug_generator(instance.tocata)

    location = 'tocata/tickets/{}/'.format(slug)
    return location + filename

class TocataTicketFile(models.Model):
    tocata              = models.ForeignKey(Tocata, on_delete=models.CASCADE)
    file                = models.FileField(
                            upload_to=upload_tocata_ticket_file_loc,
                            storage=FileSystemStorage(location=settings.PROTECTED_ROOT)
                            )

    def __str__(self):
        return self.file.name

    def get_default_url(sefl):
        return self.tocata.get_absolute_url()

    def get_donwload_url(self):
        return reverse('tocata:download',
            kwargs={'slug': self.tocata.slug, 'pk': self.pk}
            )

    @property
    def nombre(self):
        return os.path.basename(self.file.name)
