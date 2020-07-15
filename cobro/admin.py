from django.contrib import admin

from cobro.models import Carro, Orden, OrdenTocata
# Register your models here.

admin.site.register(Carro)
admin.site.register(Orden)
admin.site.register(OrdenTocata)
