from django.contrib import admin

from .models import OrdenCompra, Cobro, ControlCobro, EntradasCompradas

# Register your models here.
admin.site.register(OrdenCompra)
admin.site.register(Cobro)
admin.site.register(ControlCobro)
admin.site.register(EntradasCompradas)
