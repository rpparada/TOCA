from django.contrib import admin
from .models import Lugar, Region, Provincia, Comuna

# Register your models here.
admin.site.register(Lugar)
admin.site.register(Region)
admin.site.register(Provincia)
admin.site.register(Comuna)
