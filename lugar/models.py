from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.

# Lugares
class LugarQuerySet(models.query.QuerySet):
    def disponible(self):
        return self.filter(estado__in = ['disponible'])

    def by_request(self, request):
        return self.filter(usuario=request.user)

class LugarManager(models.Manager):
    def get_queryset(self):
        return LugarQuerySet(self.model, using=self._db)

    def disponible(self):
        return self.get_queryset().disponible()

    def by_request(self, request):
        return self.get_queryset().by_request(request).disponible().order_by('-fecha_crea')

LUGAR_ESTADO_OPCIONES = (
    ('disponible','Disponible'),
    ('noDisponible','No Disponible'),
)

class Lugar(models.Model):

    nombre          = models.CharField(max_length=200, blank=True)
    usuario         = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nombre_calle    = models.CharField(max_length=200)
    numero          = models.IntegerField()
    region          = models.ForeignKey('Region', on_delete=models.DO_NOTHING)
    provincia       = models.ForeignKey('Provincia', null=True, blank=True, on_delete=models.DO_NOTHING)
    comuna          = models.ForeignKey('Comuna', on_delete=models.DO_NOTHING)
    ciudad          = models.CharField(max_length=200, blank=True)
    pais            = models.CharField(max_length=100, default='Chile')
    codigo_postal   = models.CharField(max_length=20, blank=True)
    departamento    = models.CharField(max_length=20, blank=True)
    otros           = models.CharField(max_length=20, blank=True)

    descripción     = models.TextField(blank=True)
    capacidad       = models.IntegerField()

    estado          = models.CharField(max_length=20, choices=LUGAR_ESTADO_OPCIONES,default='disponible')
    fecha_crea      = models.DateTimeField(auto_now_add=True)
    fecha_actu      = models.DateTimeField(auto_now=True)

    objects         = LugarManager()

    def __str__(self):
        if self.nombre:
            return self.nombre+', '+self.nombre_calle+' '+str(self.numero)+', '+str(self.comuna)+' - aforo '+str(self.capacidad)
        else:
            return self.nombre_calle+' '+str(self.numero)+', '+str(self.comuna)+' - aforo '+str(self.capacidad)


# Regiones
class Region(models.Model):

    codigo          = models.CharField(max_length=100)
    nombre          = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Provincias
class Provincia(models.Model):

    region          = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)

    codigo          = models.CharField(max_length=100)
    nombre          = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Comuna
class Comuna(models.Model):

    provincia       = models.ForeignKey(Provincia, on_delete=models.DO_NOTHING, null=True)
    region          = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True)

    codigo          = models.CharField(max_length=100)
    nombre          = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
