from django.contrib import admin

from .models import AnulacionEntrada, TocataCancelada

# Register your models here.

class TocataCanceladaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'motivo', 'estado']
    class Meta:
        model = TocataCancelada

admin.site.register(TocataCancelada, TocataCanceladaAdmin)

class AnulacionEntradaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'estado']

    class Meta:
        model = AnulacionEntrada

admin.site.register(AnulacionEntrada, AnulacionEntradaAdmin)
