from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.db.models import Q, F
from django.core.files.storage import FileSystemStorage
from django.urls import reverse


from django_resized import ResizedImageField

import os
from datetime import timedelta, datetime
from django.utils import timezone

from artista.models import Artista, Estilo
from lugar.models import Lugar, Region, Comuna

from toca.utils  import unique_slug_generator

User = settings.AUTH_USER_MODEL
# Create your models here.

# Tocatas
class TocataQuerySet(models.query.QuerySet):

    def estado_disp(self):
        return self.filter(estado__in = ['publicado','confirmado','vendido'])

    def entrada_disp(self):
        return self.filter(asistentes_max__gt = F('asistentes_total'))

    def fecha_disp(self):
        return self.filter(fecha__gte = datetime.now().date())

    def disponible(self):
        return self.estado_disp().entrada_disp().fecha_disp()

    def no_disponible(self):
        return self.filter(estado__in = ['suspendido','completado'])

    def busqueda(self, consulta):
        lookups = (Q(nombre__icontains=consulta) |
                    Q(descripción__icontains=consulta) |
                    Q(artista__nombre__icontains=consulta) |
                    Q(estilos__nombre__icontains=consulta)
                    )
        return self.filter(lookups).distinct()

    def tocataartista(self, artista):
        return self.filter(artista=artista)

    def tocataartista_by_request(self, request):
        artista = Artista.objects.get(usuario=request.user)
        return self.filter(artista=artista)

    def quita_barradas(self):
        return self.exclude(estado='borrado')

class TocataManager(models.Manager):
    def get_queryset(self):
        return TocataQuerySet(self.model, using=self._db)

    def disponible(self):
        return self.get_queryset().disponible()

    def no_disponible(self):
        return self.get_queryset().no_disponible()

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

    def tocataartista_by_request(self, request):
        return self.get_queryset().tocataartista_by_request(request).quita_barradas()


def upload_tocata_flayer_file_loc(instance, filename):
    slug =instance.slug
    if not slug:
        slug = unique_slug_generator(instance)

    location = 'tocata/fotos/{}/'.format(slug)
    return location + filename

TOCATA_ESTADO_OPCIONES = (
    ('publicado', 'Publicado'),     # Publicacion inicial de tocata
    ('suspendido', 'Suspendido'),   # Tocata suspendida
    ('confirmado', 'Confirmado'),   # Quorum alcanzado
    ('vendido', 'Vendido'),         # Todas las entradas vendidas
    ('completado', 'Completado'),   # Tocata realizada
    ('borrado', 'Borrado'),         # Tocata borrada
)

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
    #flayer_380_507      = ResizedImageField(size=[380, 507],upload_to=upload_tocata_flayer_file_loc, blank=True, default='fotos/defecto/imagen_380_507.jpg')
    flayer_380_507      = ResizedImageField(size=[380, 507],upload_to=upload_tocata_flayer_file_loc, blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_380_507.jpg')
    estilos             = models.ManyToManyField(Estilo, blank=True)
    estado              = models.CharField(max_length=20, choices=TOCATA_ESTADO_OPCIONES,default='publicado')

    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    objects             = TocataManager()

    def get_absolute_url(self):
        return "/tocatas/{slug}".format(slug=self.slug)

    def __str__(self):
        return str(self.id)+' '+self.nombre

    def check_vigencia(self):
        esta_vigente = False
        estados_vig = [
            'publicado',
            'confirmado'
        ]
        if self.estado in estados_vig:
            esta_vigente = True
        return esta_vigente

    def check_entradas(self, entradas):
        entradas_disp = False
        cantidad_disp = self.asistentes_max - self.asistentes_total
        if entradas <= cantidad_disp:
            entradas_disp = True
        return entradas_disp

    def check_fechahora(self):
        a_tiempo = False
        if (timezone.now().date() - self.fecha) <= timedelta(days=0):
            a_tiempo = True
        return a_tiempo

    def suspender_tocata(self):
        fue_suspendido = False
        if self.estado in ['publicado','confirmado','vendido']:
            self.estado = 'suspendido'
            self.save()
            fue_suspendido = True
            # Agregar aqui los cambio necesarios para suspender tocata
            # - Notificar asistentes con emial
            # - Devolver dinero

        return fue_suspendido

    def borrar_tocata(self):
        fue_borrada = False
        if self.estado in ['suspendido','completado']:
            self.estado = 'borrado'
            self.save()
            fue_borrada = True

        return fue_borrada

    @property
    def name(self):
        return self.nombre

    # Tag posibles de productos
    # "product-new" = Nuevo
    # "product-sale"
    # "product-sale-off"
    # "product-out-stock"
    # "product-hot" = Confirmado
    @property
    def tagname(self):
        tag = None
        if self.asistentes_total >= self.asistentes_min:
            tag = 'product-hot'
        elif (timezone.now() - self.fecha_crea) < timedelta(days=7):
            tag = 'product-new'

        return tag

    @property
    def tagmsg(self):
        msg = None
        if self.asistentes_total >= self.asistentes_min:
            msg = 'Confirmado'
        elif (timezone.now() - self.fecha_crea) < timedelta(days=7):
            msg = 'Nuevo'
        return msg


def tocata_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tocata_pre_save_receiver, sender=Tocata)
