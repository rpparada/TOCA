from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.db.models import Q

from django_resized import ResizedImageField

from artista.models import Artista, Estilo
from lugar.models import Lugar, Region, Comuna
from tocata.models import Tocata

from toca.utils  import unique_slug_generator

from toca.parametros import parToca

User = settings.AUTH_USER_MODEL
# Create your models here.

# Tocatas Abiertas
TOCATAABIERTA_ESTADO_OPCIONES = (
    ('publicado','Publicado'),
    ('suspendido','Suspendido'),
    ('confirmado','Confirmado'),
    ('borrado','Borrado'),
)

class TocataAbiertaQuerySet(models.query.QuerySet):

    def disponible(self):
        return self.filter(estado='publicado')

    def busqueda(self, consulta):
        lookups = (Q(nombre__icontains=consulta) |
                    Q(descripción__icontains=consulta) |
                    Q(artista__nombre__icontains=consulta) |
                    Q(estilos__nombre__icontains=consulta)
                    )
        return self.filter(lookups).distinct()

    def by_artista(self, artista):
        return self.filter(artista=artista)

class TocataAbiertaManager(models.Manager):

    def get_queryset(self):
        return TocataAbiertaQuerySet(self.model, using=self._db)

    def disponible(self):
        return self.get_queryset().disponible()

    def busqueda(self, consulta):
        return self.get_queryset().disponible().busqueda(consulta)

    def get_mejores_tocatasabiertas(self, num_muestra):
        # Por ahora el criterio de mejores tocatas solo contemplara la fecha de creacion
        qs = self.get_queryset().disponible().order_by('-fecha_crea')[:num_muestra]
        if qs:
            return qs
        return self.none()

    def by_artista(self, artista):
        qs = self.get_queryset().by_artista(artista).disponible()
        if qs:
            return qs
        return self.none()

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
    estado              = models.CharField(max_length=20, choices=TOCATAABIERTA_ESTADO_OPCIONES,default='publicado')

    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    objects             = TocataAbiertaManager()

    def get_absolute_url(self):
        return "/ofrecetucasa/{slug}".format(slug=self.slug)

    def __str__(self):
        return self.nombre

def tocataabierta_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tocataabierta_pre_save_receiver, sender=TocataAbierta)
