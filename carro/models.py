from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, pre_save

from tocata.models import Tocata

# Create your models here.

# Carro Comprar
class CarroCompraManager(models.Manager):

    def new_or_get(self, request):
        carro_id =request.session.get('carro_id', None)
        qs = self.get_queryset().filter(id=carro_id)
        if qs.count() == 1:
            nuevo_obj = False
            carro_obj = qs.first()
            if request.user.is_authenticated and carro_obj.usuario is None:
                carro_obj.usuario = request.user
                carro_obj.save()
        else:
            nuevo_obj = False
            carro_obj = CarroCompra.objects.nuevo(user=request.user)
            request.session['carro_id'] = carro_obj.id

        return carro_obj, nuevo_obj

    def nuevo(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user

        return self.model.objects.create(usuario=user_obj)

class CarroCompra(models.Model):

    usuario             = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    tocata              = models.ManyToManyField(Tocata, blank=True)
    cantidad            = models.IntegerField(default=0)
    subtotal            = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    fecha_actu          = models.DateTimeField(auto_now=True)
    fecha_crea          = models.DateTimeField(auto_now_add=True)

    objects             = CarroCompraManager()

    def __str__(self):
        return str(self.id)

def m2m_changed_carro_receiver(sender, instance, action, *args, **kwargs):

    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        tocatas = instance.tocata.all()
        total = 0
        for tocata in tocatas:
            total += tocata.costo
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_carro_receiver, sender=CarroCompra.tocata.through)

def pre_save_carro_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10
    else:
        instance.total = 0.00

pre_save.connect(pre_save_carro_receiver, sender=CarroCompra)
