from django.contrib import admin

from .models import OrdenCompra, Cobro, ControlCobro

# Register your models here.

admin.site.register(OrdenCompra)
admin.site.register(Cobro)
admin.site.register(ControlCobro)
