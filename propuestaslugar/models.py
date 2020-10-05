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

    def para_borrar(self):
        return self.filter(estado__in=['cancelado','completado','noelegido'])

    def elegidas(self):
        return self.filter(estado__in=['elegido',])

    def by_tocataabierta(self, tocataabierta):
        return self.filter(tocataabierta=tocataabierta)

    def by_lugar(self, lugar):
        return self.filter(lugar=lugar)

    def sin_borrado_cancelado(self):
        return self.exclude(estado__in=['cancelado', 'borrado',])

    def existe(self, tocataabierta, lugar):
        qs = self.by_tocataabierta(tocataabierta).by_lugar(lugar).sin_borrado_cancelado()
        if qs.exists():
            return qs.first()
        return None

    def ver_propuestas(self, tocataabierta_id):
        return self.filter(tocataabierta=tocataabierta_id).filter(estado='pendiente').order_by('-fecha_crea')

class LugaresTocataManager(models.Manager):
    def get_queryset(self):
        return LugaresTocataQuerySet(self.model, using=self._db)

    def mis_propuestas_by_request(self, request):
        return self.get_queryset().mis_propuestas_by_request(request).sin_borradas().order_by('-fecha_crea')

    def para_borrar_by_request(self, request):
        return self.get_queryset().mis_propuestas_by_request(request).para_borrar().sin_borradas()

    def elegidas_by_request(self, request):
        return self.get_queryset().mis_propuestas_by_request(request).elegidas()

    def existe(self, tocataabierta, lugar):
        return self.get_queryset().existe(tocataabierta, lugar)

    def new_or_get(self, tocataabierta, lugar):
        obj = self.get_queryset().existe(tocataabierta, lugar)
        created = False
        if not obj:
            obj = self.model.objects.create(
                                        tocataabierta=tocataabierta,
                                        lugar=lugar
                                    )
            created = True

        return obj, created

    def ver_propuestas(self, tocataabierta_id):
        return self.get_queryset().ver_propuestas(tocataabierta_id)

LUGARESTOCATA_ESTADO_OPCIONES = (
    ('elegido','Elegido'),
    ('noelegido','No Elegido'),
    ('pendiente','Pendiente'),
    ('cancelado','Cancelado'),
    ('completado','Completado'),
    ('borrado','Borrado'),
)

class LugaresTocata(models.Model):

    tocataabierta       = models.ForeignKey(TocataAbierta, on_delete=models.CASCADE)
    lugar               = models.ForeignKey(Lugar, on_delete=models.CASCADE)

    estado              = models.CharField(max_length=20, choices=LUGARESTOCATA_ESTADO_OPCIONES,default='pendiente')
    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    objects             = LugaresTocataManager()

    def __str__(self):
        return self.tocataabierta.nombre+' - '+str(self.lugar.nombre_calle)+' '+str(self.lugar.numero)

    def cancelar(self):
        fue_cancelado = False
        if self.estado in ['pendiente',]:
            self.estado = 'cancelado'
            self.save()
            fue_cancelado = True

        return fue_cancelado

    def borrar(self):
        fue_borrado = False
        if self.estado in ['noelegido', 'cancelado','completado', ]:
            self.estado = 'borrado'
            self.save()
            fue_borrado = True

        return fue_borrado

    def cancelar_elegido(self):
        fue_cancelado = False
        if self.estado in ['elegido',]:
            self.estado = 'cancelado'
            self.save()
            fue_cancelado = True

        return fue_cancelado
