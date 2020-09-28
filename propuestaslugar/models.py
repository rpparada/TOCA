from django.db import models

from tocataabierta.models import TocataAbierta
from lugar.models import Lugar
# Create your models here.

# Lugares Tocata
class LugaresTocataQuerySet(models.query.QuerySet):
    def mis_propuestas_by_request(self, request):
        return self.filter(lugar__usuario=request.user)

    def sin_borradas(self):
        return self.exclude(estado__in=['borrado',])

class LugaresTocataManager(models.Manager):
    def get_queryset(self):
        return LugaresTocataQuerySet(self.model, using=self._db)

    def mis_propuestas_by_request(self, request):
        return self.get_queryset().mis_propuestas_by_request(request).sin_borradas().order_by('-fecha_crea')

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

    estado              = models.CharField(max_length=20, choices=LUGARESTOCATA_ESTADO_OPCIONES,default='pendiente')
    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    objects             = LugaresTocataManager()

    def __str__(self):
        return self.tocataabierta.nombre+' - '+str(self.lugar.nombre_calle)+' '+str(self.lugar.numero)
