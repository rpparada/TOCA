from django.db import models

from artista.models import Artista

# Create your models here.

class Testimonios(models.Model):

    artista = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)
    Testimonio = models.CharField(max_length=200)
