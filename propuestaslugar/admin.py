from django.contrib import admin

from .models import LugaresTocata

# Register your models here.
class LugaresTocataAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'estado']

    class Meta:
        model = LugaresTocata

admin.site.register(LugaresTocata, LugaresTocataAdmin)
