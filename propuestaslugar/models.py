from django.db import models

from tocataabierta.models import TocataAbierta
from lugar.models import Lugar
# Create your models here.

# Lugares Tocata
LUGARESTOCATA_ESTADO_OPCIONES = (
    ('elegido','Elegido'),
    ('noelegido','No Elegido'),
    ('pendiente','Pendiente'),
    ('cancelado','Cancelado'),
    ('completado','Completado'),
    ('borrado','Borrado'),
)

class LugaresTocata(models.Model):

    tocataabierta       = models.ForeignKey(TocataAbierta, on_delete=models.DO_NOTHING)
    lugar               = models.ForeignKey(Lugar, on_delete=models.DO_NOTHING)

    estado              = models.CharField(max_length=2, choices=LUGARESTOCATA_ESTADO_OPCIONES,default='pendiente')
    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tocataabierta.nombre+' - '+str(self.lugar.nombre_calle)+' '+str(self.lugar.numero)
