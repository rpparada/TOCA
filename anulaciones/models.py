from django.db import models

from orden.models import EntradasCompradas, Cobro

# Create your models here.

# Tocata Cancelada
class TocataCanceladaQuerySet(models.query.QuerySet):
    def pendientes(self):
        return self.filter(estado='pendiente')

class TocataCanceladaManager(models.Manager):
    def get_queryset(self):
        return TocataCanceladaQuerySet(self.model, self._db)

    def pendientes(self):
        return self.get_queryset().pendientes()

    def new_or_get(self, tocata, motivo='artista'):
        qs = self.get_queryset().filter(tocata=tocata)
        if qs.count() == 1:
            nuevo_obj = False
            cancelacion_obj = qs.first()
        else:
            nuevo_obj = True
            cancelacion_obj = TocataCancelada.objects.create(tocata=tocata, motivo=motivo)

        return cancelacion_obj, nuevo_obj

TOCATACANCELADA_ESTADO_OPCIONES = (
    ('pendiente','Pendiente'),
    ('reembolsado','Reembolsado'),
)

TOCATACANCELADA_MOTIVO_OPCIONES = (
    ('artista','Suspendido por Artista'),
    ('anfitrion','Anfitrio canceló Lugar'),
    ('otro','Otro'),
)

class TocataCancelada(models.Model):

    tocata                  = models.ForeignKey('tocata.Tocata', on_delete=models.CASCADE)
    motivo                  = models.CharField(max_length=20, choices=TOCATACANCELADA_MOTIVO_OPCIONES, default='artista')

    estado                  = models.CharField(max_length=20, choices=TOCATACANCELADA_ESTADO_OPCIONES, default='pendiente')
    fecha_actu              = models.DateTimeField(auto_now=True)
    fecha_crea              = models.DateTimeField(auto_now_add=True)

    objects                 = TocataCanceladaManager()

    def __str__(self):
        return str(self.tocata)


# Anulaciones Entradas
class AnulacionEntradaQuerySet(models.query.QuerySet):
    def pendientes(self):
        return self.filter(estado='pendiente')

    def by_tocata(self, tocata):
        return self.filter(entradas_compradas__item__tocata=tocata)

class AnulacionEntradaManager(models.Manager):
    def get_queryset(self):
        return AnulacionEntradaQuerySet(self.model, self._db)

    def pendientes(self):
        return self.get_queryset().pendientes()

    def new_or_get(self, entradas, cobro):
        qs = self.get_queryset().filter(entradas_compradas=entradas)
        if qs.count() == 1:
            nuevo_obj = False
            anulacion_obj = qs.first()
        else:
            nuevo_obj = True
            anulacion_obj = AnulacionEntrada.objects.create(entradas_compradas=entradas, cobro=cobro)

        return anulacion_obj, nuevo_obj

    def by_tocata(self, tocata):
        return self.get_queryset().by_tocata(tocata)

# Para tarjeta de crédito pueden ser los siguientes tipos de pago (con las abreviaciones entre paréntesis):
# - Venta Normal (VN): Pago en 1 cuota.
# - 2 Cuotas sin interés (S2): El comercio recibe el pago en 2 cuotas iguales sin interés.
# - 3 Cuotas sin interés (SI): El comercio recibe el pago en 3 cuotas iguales sin interés.
# - N Cuotas sin interés (NC): El comercio recibe el pago en un número de cuotas iguales y sin interés que el tarjetahabiente puede elegir de entre un rango de 2 y N (el valor N es definido por el comercio y no puede ser superior a 12)
# - Cuotas normales (VC): El emisor ofrece al tarjetahabiente entre 2 y 48 cuotas. El emisor define si son sin interés (si ha establecido un rango de cuotas en promoción) o con interés. El emisor también puede ofrecer de 1 hasta 3 meses de pago diferida. Todo esto sin impacto para el comercio que en esta modalidad de cuotas siempre recibe el pago en 48 horas hábiles.

# Para tarjeta de débito Redcompra el tipo de pago siempre corresponde a:
# - Venta débito Redcompra (VD): Pago con tarjeta de débito Redcompra.
# - Venta Prepago (VP): Pago con tarjeta de débito Redcompra.

ANULACIONENTRADA_ESTADO_OPCIONES = (
    ('pendiente','Pendiente'),
    ('enviadatbk','Enviada a Transbank'),
    ('reembolsado','Reembolsado'),
)

class AnulacionEntrada(models.Model):

    entradas_compradas      = models.ForeignKey(EntradasCompradas, on_delete=models.CASCADE)
    cobro                   = models.ForeignKey(Cobro, on_delete=models.CASCADE)

    estado                  = models.CharField(max_length=20, choices=ANULACIONENTRADA_ESTADO_OPCIONES,default='pendiente')
    fecha_actu              = models.DateTimeField(auto_now=True)
    fecha_crea              = models.DateTimeField(auto_now_add=True)

    objects                 = AnulacionEntradaManager()

    def __str__(self):
        return str(self.entradas_compradas)
