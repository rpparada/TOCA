from django.contrib import admin
from .models import Lugar, Region, Provincia, Comuna

# Register your models here.

class LugarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'usuario', 'capacidad', 'estado', 'fecha_crea']
    class Meta:
        model = Lugar

admin.site.register(Lugar, LugarAdmin)
admin.site.register(Region)
admin.site.register(Provincia)
admin.site.register(Comuna)
