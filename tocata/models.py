from django.db import models
from django.contrib.auth.models import User

from artista.models import Artista
from lugar.models import Lugar, Region, Comuna


from django_resized import ResizedImageField

from toca.parametros import parToca, parTocatas, parLugaresToc, parTocatasAbiertas

# Create your models here.
class Tocata(models.Model):

    artista             = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)
    usuario             = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nombre              = models.CharField(max_length=200)
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

    estado              = models.CharField(max_length=2, choices=parTocatas['estado_tipos'],default=parToca['publicado'])
    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class TocataAbierta(models.Model):

    artista             = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)
    usuario             = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nombre              = models.CharField(max_length=200)
    region              = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True, blank=True)
    comuna              = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING, null=True, blank=True)
    descripción         = models.TextField(blank=True)
    costo               = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    fecha               = models.DateField()
    hora                = models.TimeField()
    asistentes_min      = models.IntegerField()
    flayer_original     = models.ImageField(upload_to='fotos/tocatas/%Y/%m/%d/', blank=True, default='fotos/defecto/imagen_original.jpg')
    flayer_1920_1280    = ResizedImageField(size=[1920, 1280],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_1920_1280.jpg')
    flayer_380_507      = ResizedImageField(size=[380, 507],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_380_507.jpg')

    tocata              = models.ForeignKey(Tocata, on_delete=models.DO_NOTHING, null=True, blank=True)

    estado              = models.CharField(max_length=2, choices=parTocatasAbiertas['estado_tipos'],default=parToca['publicado'])
    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class LugaresTocata(models.Model):

    tocataabierta       = models.ForeignKey(TocataAbierta, on_delete=models.DO_NOTHING)
    lugar               = models.ForeignKey(Lugar, on_delete=models.DO_NOTHING)

    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)
    estado              = models.CharField(max_length=2, choices=parLugaresToc['estado_lugartocata'],default=parToca['pendiente'])

    def __str__(self):
        return self.tocataabierta.nombre+' - '+str(self.lugar.nombre_calle)+' '+str(self.lugar.numero)
