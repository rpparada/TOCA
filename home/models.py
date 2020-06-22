from django.db import models

from artista.models import Artista

from toca.parametros import parToca, parTestimonios

# Create your models here.

class Testimonios(models.Model):

    artista = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)
    testimonio = models.CharField(max_length=120, blank=True)
    objetivo = models.CharField(max_length=2, choices=parTestimonios['objetivos_tipos'],default=parToca['usuarios'])

    foto = models.ImageField(upload_to='fotos/testimonios/%Y/%m/%d/', blank=True)

    estado = models.CharField(max_length=2, choices=parTestimonios['estado_tipos'],default=parToca['disponible'])
    fecha_crea = models.DateTimeField(auto_now_add=True)
    fecha_actua = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.artista)+'('+str(self.objetivo)+'): '+str(self.testimonio[:100])
