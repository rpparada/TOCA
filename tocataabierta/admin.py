from django.contrib import admin

from .models import TocataAbierta

# Register your models here.

class TocataAbiertaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'id']

    class Meta:
        model = TocataAbierta

admin.site.register(TocataAbierta, TocataAbiertaAdmin)
