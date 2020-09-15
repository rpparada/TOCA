from django.contrib import admin
from .models import Tocata

# Register your models here.


class TocataAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'fecha', 'asistentes_total', 'asistentes_max', 'estado']
    class Meta:
        model = Tocata

admin.site.register(Tocata, TocataAdmin)
