from django.db import models
from django.contrib.auth.models import User

from tocata.models import Tocata

# Create your models here.
class CarroCompra(models.Model):

    usuario             = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    tocata              = models.ManyToManyField(Tocata, blank=True)
    cantidad            = models.IntegerField(default=0)
    total               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
