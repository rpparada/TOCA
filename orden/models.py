from django.db import models
from django.db.models.signals import pre_save, post_save

from carro.models import CarroCompra

from toca.utils import unique_orden_id_generator
from toca.parametros import parToca, parCarro, parOrden, mediodepago

# Create your models here.


# Orden Compra
class OrdenCompra(models.Model):

    orden_id            = models.CharField(max_length=120, blank=True)

    carro               = models.ForeignKey(CarroCompra, on_delete=models.DO_NOTHING)
    total               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    envio               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    estado              = models.CharField(max_length=2, choices=parOrden['estado_orden'],default=parToca['pendiente'])
    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.orden_id

    def actualiza_total(self):
        carro_total = self.carro.total
        envio_total = self.envio
        nuevo_total =carro_total + envio_total
        self.total = nuevo_total
        self.save()
        return nuevo_total

def pre_save_ordencompra_receiver(sender, instance, *args, **kwargs):
    if not instance.orden_id:
        instance.orden_id = unique_orden_id_generator(instance)

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
