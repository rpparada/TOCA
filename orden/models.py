from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.core.files import File
from django.utils import timezone
from django.contrib import messages

User = settings.AUTH_USER_MODEL

import math
import os

from carro.models import CarroCompra, ItemCarroCompra
from facturacion.models import FacturacionProfile
from direccion.models import Direccion

from toca.utils import unique_orden_id_generator, unique_slug_generator, render_to_pdf_file
from toca.parametros import parCarro, parOrden, mediodepago

# Create your models here.

# Orden Compra
class OrdenCompraQuerySet(models.query.QuerySet):
    def by_request(self, request):
        fact_profile, created = FacturacionProfile.objects.new_or_get(request)
        return self.filter(facturacion_profile=fact_profile)

    def by_orden_id(self, orden_id):
        qs = self.filter(orden_id=orden_id)
        obj = None
        if qs.count() == 1:
            obj = qs.first()
        return obj

class OrdenCompraManager(models.Manager):
    def get_queryset(self):
        return OrdenCompraQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, fact_profile, carro_obj):
        created = False
        qs = self.get_queryset().filter(facturacion_profile=fact_profile, carro=carro_obj, activo=True, estado='pendiente')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(facturacion_profile=fact_profile, carro=carro_obj)
            created = True
        return obj, created

    def by_orden_id(self, orden_id):
        return self.get_queryset().by_orden_id(orden_id)

ORDENCOMPRA_ESTADO_OPCIONES = (
    ('pendiente','Pendiente'),
    ('pagado','Pagado'),
    ('cancelado','Cancelado'),
)

class OrdenCompra(models.Model):

    orden_id                = models.CharField(max_length=120, blank=True)
    facturacion_profile     = models.ForeignKey(FacturacionProfile, null=True, blank=True, on_delete=models.CASCADE)
    direccion_envio         = models.ForeignKey(Direccion, related_name='direccion_envio', null=True, blank=True, on_delete=models.CASCADE)
    direccion_facturacion   = models.ForeignKey(Direccion, related_name='direccion_facturacion', null=True, blank=True, on_delete=models.CASCADE)
    email_adicional         = models.EmailField(null=True, blank=True)
    carro                   = models.ForeignKey(CarroCompra, on_delete=models.DO_NOTHING)
    total                   = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    envio                   = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    activo                  = models.BooleanField(default=True)
    fecha_pago              = models.DateTimeField(null=True, blank=True)

    estado                  = models.CharField(max_length=20, choices=ORDENCOMPRA_ESTADO_OPCIONES,default='pendiente')
    fecha_actu              = models.DateTimeField(auto_now=True)
    fecha_crea              = models.DateTimeField(auto_now_add=True)

    objects                 = OrdenCompraManager()

    def __str__(self):
        return self.orden_id

    def actualiza_total(self):
        carro_total = self.carro.total
        envio_total = self.envio
        nuevo_total = math.fsum([carro_total, envio_total])
        self.total = nuevo_total
        self.save()
        return nuevo_total

    def check_done(self, request):

        is_done = True

        for item in self.carro.item.all():
            # Verificar estado de tocata
            if item.tocata.check_vigencia():
                pass
            else:
                is_done = False
                self.carro.item.remove(item)
                messages.error(request,'Tocata ya no esta dispinible')

            # Agregar verificacion de venta de entradas disponibles
            if item.tocata.check_entradas(item.cantidad):
                pass
            else:
                is_done = False
                self.carro.item.remove(item)
                messages.error(request,'No hay suficientes entradas disponibles')

            # Comprar antes de la fecha y hora del evento
            if item.tocata.check_fechahora():
                pass
            else:
                is_done = False
                self.carro.item.remove(item)
                messages.error(request,'Compra fuera de tiempo')

        facturacion_profile = self.facturacion_profile
        total = self.total
        if facturacion_profile and total <= 0:
            is_done = False

        return is_done

    def actualiza_compras(self):
        for item in self.carro.item.all():
            obj, created = EntradasCompradas.objects.get_or_create(
                        orden = self,
                        facturacion_profile = self.facturacion_profile,
                        item = item
            )
        return EntradasCompradas.objects.filter(orden=self).count()

    def agrega_entradas_compra(self):
        entradas_obj = EntradasCompradas.objects.by_orden(self)
        if entradas_obj:
            for entrada_obj in entradas_obj:
                context = {
                    'boleta_id': 8838838,
                    'nombre_cliente': 'Rodrigo Parada',
                    'cantidad': 29939,
                    'fecha_compra': 'Hoy'
                }
                #pdf = render_to_pdf('carro/entradaspdf.html', context)
                pdf = render_to_pdf_file('carro/entradaspdf.html', context, 'test.pdf')
                # Falta salvar a un archivo antes de guardarlo en la tabla
                f = open('nuevotest.pdf', 'wb')
                myfile = File(f)
                myfile = ContentFile(pdf)
                entrada_obj.file.save('nuevotest.pdf', myfile)
                #entrada_obj.save()


    def mark_pagado(self):
        if self.estado != 'pagado':
            if self.check_done():
                self.estado = 'pagado'
                self.fecha_pago = timezone.now()
                self.save()
                self.actualiza_compras()

        return self.estado

    def guarda_cobro(self, transaction, token):
        cobro_obj = Cobro.objects.create(
            orden               = self,
            facturacion_profile = self.facturacion_profile,
            token               = token,
            accountingDate      = transaction['accountingDate'],
            buyOrder            = transaction['buyOrder'],
            cardNumber          = transaction['cardDetail']['cardNumber'],
            cardExpirationDate  = transaction['cardDetail']['cardExpirationDate'],
            sharesAmount        = transaction['detailOutput'][0]['sharesAmount'],
            sharesNumber        = transaction['detailOutput'][0]['sharesNumber'],
            amount              = transaction['detailOutput'][0]['amount'],
            commerceCode        = transaction['detailOutput'][0]['commerceCode'],
            authorizationCode   = transaction['detailOutput'][0]['authorizationCode'],
            paymentTypeCode     = transaction['detailOutput'][0]['paymentTypeCode'],
            responseCode        = transaction['detailOutput'][0]['responseCode'],
            sessionId           = transaction['sessionId'],
            transactionDate     = transaction['transactionDate'],
            urlRedirection      = transaction['urlRedirection'],
            vci                 = transaction['VCI'],
        )

        return cobro_obj

    def sumar_asistentes_total(self):
        for item in self.carro.item.all():
            item.tocata.asistentes_total += item.cantidad
            item.tocata.save()

    def limpia_carro(self):
        self.carro.vigente = False
        self.carro.save()

def pre_save_ordencompra_receiver(sender, instance, *args, **kwargs):
    if not instance.orden_id:
        instance.orden_id = unique_orden_id_generator(instance)
    qs = OrdenCompra.objects.filter(carro=instance.carro).exclude(facturacion_profile=instance.facturacion_profile)
    if qs.exists():
        qs.update(activo=False)

pre_save.connect(pre_save_ordencompra_receiver, sender=OrdenCompra)

def post_save_carro_total(sender, instance, created, *args, **kwargs):

    if not created:
        carro_obj = instance
        carro_total = carro_obj.total
        carro_id = carro_obj.id
        qs = OrdenCompra.objects.filter(carro__id=carro_id)
        if qs.count() == 1:
            orden_obj = qs.first()
            orden_obj.actualiza_total()

post_save.connect(post_save_carro_total, sender=CarroCompra)

def post_save_orden(sender, instance, created, *args, **kwargs):
    if created:
        instance.actualiza_total()

post_save.connect(post_save_orden, sender=OrdenCompra)

# Cobro Transbank
class CobroQuerySet(models.query.QuerySet):
    def by_orden(self, orden):
        return self.filter(orden=orden)

    def by_token(self, token):
        return self.filter(token=token)

class CobroManager(models.Manager):
    def get_queryset(self):
        return CobroQuerySet(self.model, using=self._db)

    def by_orden(self, orden):
        return self.get_queryset().by_orden(orden)

    def by_token(self, token):
        return self.get_queryset().by_token(token)

    def new_or_get(self, orden):
        created = False
        qs = self.get_queryset().by_orden(orden)
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(orden=orden)
            created = True

        return obj, created

class Cobro(models.Model):

    orden                   = models.ForeignKey(OrdenCompra, on_delete=models.DO_NOTHING)
    facturacion_profile     = models.ForeignKey(FacturacionProfile, null=True, blank=True, on_delete=models.CASCADE)

    token                   = models.CharField(max_length=64, blank=True, null=True)
    accountingDate          = models.CharField(max_length=4, blank=True, null=True)
    buyOrder                = models.CharField(max_length=26, blank=True, null=True)
    cardNumber              = models.CharField(max_length=16, blank=True, null=True)
    cardExpirationDate      = models.CharField(max_length=4, blank=True, null=True)
    sharesAmount            = models.CharField(max_length=10, blank=True, null=True)
    sharesNumber            = models.CharField(max_length=2, blank=True, null=True)
    amount                  = models.CharField(max_length=10, blank=True, null=True)
    commerceCode            = models.CharField(max_length=12, blank=True, null=True)
    authorizationCode       = models.CharField(max_length=6, blank=True, null=True)
    paymentTypeCode         = models.CharField(max_length=3, blank=True, null=True)
    responseCode            = models.CharField(max_length=2, blank=True, null=True)
    sessionId               = models.CharField(max_length=61, blank=True, null=True)
    transactionDate         = models.DateTimeField(blank=True, null=True)
    urlRedirection          = models.CharField(max_length=256, blank=True, null=True)
    vci                     = models.CharField(max_length=3, blank=True, null=True)

    objects                 = CobroManager()

    def __str__(self):
        return str(self.orden.id)

# Control de Cobros

# Código de respuesta de la autorización. Valores posibles:
# 0 = Transacción aprobada
# -1 = Rechazo de transacción - Reintente (Posible error en el ingreso de datos de la transacción)
# -2 = Rechazo de transacción (Se produjo fallo al procesar la transacción. Este mensaje de rechazo está relacionado a parámetros de la tarjeta y/o su cuenta asociada)
# -3 = Error en transacción (Interno Transbank)
# -4 = Rechazo emisor (Rechazada por parte del emisor)
# -5 = Rechazo - Posible Fraude (Transacción con riesgo de posible fraude)
CONTROLCOBRO_ESTADO_OPCIONES = (
    ('initTransaction','initTransaction'),
    ('getTransactionResult','getTransactionResult'),
    ('acknowledgeTransaction','acknowledgeTransaction'),
    ('rechazoTransaccion_1','rechazoTransaccion_1'),
    ('rechazoTransaccion_2','rechazoTransaccion_2'),
    ('errorTransaccion','errorTransaccion'),
    ('rechazoEmisor','rechazoEmisor'),
    ('rechazoPosibleFraude','rechazoPosibleFraude'),
    ('desconocido','desconocido'),
    ('exitoso','existoso'),
)

class ControlCobroQuerySet(models.query.QuerySet):
    def by_token(self, token):
        return self.filter(token=token)

class ControlCobroManager(models.Manager):
    def get_queryset(self):
        return ControlCobroQuerySet(self.model, using=self._db)

    def by_token(self, token):
        return self.get_queryset().by_token(token)

    def new_or_get(self, token):
        created = False
        qs = self.get_queryset().by_token(token)
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(token=token)
            created = True

        return obj, created

# Control de pago con Transbank
class ControlCobro(models.Model):

    token                   = models.CharField(max_length=64)
    estado                  = models.CharField(max_length=30, choices=CONTROLCOBRO_ESTADO_OPCIONES, default='initTransaction')
    orden                   = models.ForeignKey(OrdenCompra, on_delete=models.DO_NOTHING, blank=True, null=True)

    fecha_actu              = models.DateTimeField(auto_now=True)
    fecha_crea              = models.DateTimeField(auto_now_add=True)

    objects                 = ControlCobroManager()

    def __str__(self):
        return self.token

    def actualizar_estado(self, estado):
        self.estado = estado
        self.save()

    def agregar_orden(self, orden):
        self.orden = orden
        self.save()

# Entradas Compradas
class EntradasCompradasQuerySet(models.query.QuerySet):
    def activas(self):
        return self.filter(rembolsado=False)

    def by_request(self, request):
        fact_profile, created = FacturacionProfile.objects.new_or_get(request)
        return self.filter(facturacion_profile=fact_profile)

    def by_orden(self, orden):
        return self.filter(orden=orden)

class EntradasCompradasManager(models.Manager):
    def get_queryset(self):
        return EntradasCompradasQuerySet(self.model, self._db)

    def all(self):
        return self.get_queryset().activas()

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def by_orden(self, orden):
        return self.get_queryset().by_orden(orden)

def upload_ticket_file_loc(instance, filename):
    username = instance.facturacion_profile.usuario.email
    slug = instance.item.tocata.slug
    if not slug:
        slug = unique_slug_generator(instance.item.tocata)

    location = '{0}/tickets/{1}/'.format(username,slug)
    return location + filename

class EntradasCompradas(models.Model):

    orden                   = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    facturacion_profile     = models.ForeignKey(FacturacionProfile, on_delete=models.CASCADE)
    item                    = models.ForeignKey(ItemCarroCompra, on_delete=models.CASCADE)
    rembolsado              = models.BooleanField(default=False)

    fecha_actu              = models.DateTimeField(auto_now=True)
    fecha_crea              = models.DateTimeField(auto_now_add=True)

    file                    = models.FileField(
                            upload_to=upload_ticket_file_loc,
                            storage=FileSystemStorage(location=settings.PROTECTED_ROOT),
                            null=True,
                            blank=True
                            )

    objects                 = EntradasCompradasManager()

    def __str__(self):
        return str(self.item.cantidad)+' '+str(self.item.tocata.nombre)

    def get_download_url(self):
        return reverse('ordenes:downloadticket',
            kwargs={'orden_id': self.orden.id,
                    'pk': self.pk}
            )

    @property
    def nombrearchivo(self):
        if self.file:
            return os.path.basename(self.file.name)
