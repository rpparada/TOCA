from django.db import models

from django.contrib.auth.models import User

from tocata.models import Tocata

from toca.parametros import parToca, parCarro, parOrden, mediodepago


# Create your models here.
class Orden(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    numerodeitems = models.IntegerField(default=0)
    totalapagar = models.IntegerField(default=0)
    mediodepago = models.CharField(max_length=2, choices=mediodepago['medio_de_pago'],default=parToca['webpay'])
    email = models.EmailField(blank=True)

    estado = models.CharField(max_length=2, choices=parOrden['estado_orden'],default=parToca['pendiente'])
    fecha_actu = models.DateTimeField(auto_now=True)
    fecha_crea = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.email+' '+str(self.id)+' '+str(self.numerodeitems)+' '+str(self.totalapagar)

class Carro(models.Model):

    tocata = models.ForeignKey(Tocata, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    orden = models.ForeignKey(Orden, on_delete=models.DO_NOTHING, null=True, blank=True)
    cantidad = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    estado = models.CharField(max_length=2, choices=parCarro['estado_carro'],default=parToca['pendiente'])
    fecha_actu = models.DateTimeField(auto_now=True)
    fecha_crea = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.usuario.email+' '+self.tocata.nombre+' '+str(self.cantidad)+' '+str(self.cantidad*self.tocata.costo)

class OrdenTocata(models.Model):

    orden = models.ForeignKey(Orden, on_delete=models.DO_NOTHING)
    tocata = models.ForeignKey(Tocata, on_delete=models.DO_NOTHING)
    cantidad = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    fecha_actu = models.DateTimeField(auto_now=True)
    fecha_crea = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.orden.id)+' '+str(self.tocata.nombre)

class OrdenTBK(models.Model):

    orden = models.ForeignKey(Orden, on_delete=models.DO_NOTHING)

    token = models.CharField(max_length=200, blank=True, null=True)
    accountingDate = models.CharField(max_length=200, blank=True, null=True)
    buyOrder = models.CharField(max_length=200, blank=True, null=True)
    cardNumber = models.CharField(max_length=200, blank=True, null=True)
    cardExpirationDate = models.CharField(max_length=200, blank=True, null=True)
    sharesAmount = models.CharField(max_length=200, blank=True, null=True)
    sharesNumber = models.CharField(max_length=200, blank=True, null=True)
    amount = models.CharField(max_length=200, blank=True, null=True)
    commerceCode = models.CharField(max_length=200, blank=True, null=True)
    authorizationCode = models.CharField(max_length=200, blank=True, null=True)
    paymentTypeCode = models.CharField(max_length=200, blank=True, null=True)
    responseCode = models.CharField(max_length=200, blank=True, null=True)
    sessionId = models.CharField(max_length=200, blank=True, null=True)
    transactionDate = models.CharField(max_length=200, blank=True, null=True)
    urlRedirection = models.CharField(max_length=200, blank=True, null=True)
    VCI = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.orden.id)
