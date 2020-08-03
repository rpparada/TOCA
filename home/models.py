from django.db import models
from django.db.models.signals import pre_save

from artista.models import Artista

from toca.parametros import parToca, parTestimonios

from toca.utils  import unique_slug_generator

# Create your models here.

class Testimonio(models.Model):

    artista             = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)
    slug                = models.SlugField(blank=True, unique=True)
    testimonio          = models.CharField(max_length=120, blank=True)
    objetivo            = models.CharField(max_length=2, choices=parTestimonios['objetivos_tipos'],default=parToca['usuarios'])

    estado              = models.CharField(max_length=2, choices=parTestimonios['estado_tipos'],default=parToca['disponible'])
    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.artista)+'('+str(self.objetivo)+'): '+str(self.testimonio[:100])

def testimonio_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(testimonio_pre_save_receiver, sender=Testimonio)
