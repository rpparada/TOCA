from django.db import models
from datetime import datetime
from artista.models import Artista
from lugar.models import Lugar, Region, Comuna
from django.contrib.auth.models import User

from django_resized import ResizedImageField

from toca.parametros import parToca, parTocatas, parLugaresToc

# Create your models here.
class Tocata(models.Model):

    artista = models.ForeignKey(Artista, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nombre = models.CharField(max_length=200)
    lugar = models.ForeignKey(Lugar, on_delete=models.DO_NOTHING, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.DO_NOTHING, null=True, blank=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING, null=True, blank=True)
    descripción = models.TextField(blank=True)
    costo = models.IntegerField()
    fecha = models.DateField()
    hora = models.TimeField()
    fecha_actu = models.DateTimeField(auto_now=True)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    lugar_def = models.CharField(max_length=2, choices=parTocatas['lugar_def_tipos'],default=parToca['cerrada'])
    asistentes_total = models.IntegerField(default=0)
    asistentes_min = models.IntegerField()
    asistentes_max = models.IntegerField()
    flayer_original = models.ImageField(upload_to='fotos/tocatas/%Y/%m/%d/', blank=True, default='fotos/defecto/imagen_original.jpg')
    flayer_1920_1280 = ResizedImageField(size=[1920, 1280],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_1920_1280.jpg')
    flayer_380_507 = ResizedImageField(size=[380, 507],upload_to='fotos/lugares/%Y/%m/%d/', blank=True, crop=['middle', 'center'], default='fotos/defecto/imagen_380_507.jpg')
    evaluacion = models.IntegerField(choices=parToca['valoresEvaluacion'],default=parToca['defaultEvaluacion'])
    estado = models.CharField(max_length=2, choices=parTocatas['estado_tipos'],default=parToca['inicial'])

    def __str__(self):
        return self.nombre

class LugaresTocata(models.Model):

    tocata = models.ForeignKey(Tocata, on_delete=models.DO_NOTHING)
    lugar = models.ForeignKey(Lugar, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    fecha_actu = models.DateTimeField(auto_now=True)
    fecha_crea = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=2, choices=parLugaresToc['estado_lugartocata'],default=parToca['noelegido'])

    def __str__(self):
        return self.tocata.nombre+' - '+self.lugar.nombre

# Mover estos a una nueva aplicacione para pagos
class MediosDePago(models.Model):

    nombre_proveedor = models.CharField(max_length=200)

    online = 'ON'
    caja_fisica = 'CA'
    plataformas = [
        (online,'En Linea'),
        (caja_fisica, 'Fuera de línea'),
    ]
    plataforma = models.CharField(max_length=2, choices=plataformas,default=online)

    peso_chileno = 'CLP'
    dolar_us = 'USD'
    monedas = [
        (peso_chileno,'Peso Chileno'),
        (dolar_us, 'Dolar US'),
    ]
    moneda = models.CharField(max_length=3, choices=monedas,default=peso_chileno)

    chile = 'CL'
    internacional = 'IN'
    localidades = [
        (chile,'Chile'),
        (internacional, 'Internacional'),
    ]
    ubicacion = models.CharField(max_length=2, choices=localidades,default=chile)

    formas_de_pago = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_proveedor


class CompraTocata(models.Model):

    tocata = models.ForeignKey(Tocata, on_delete=models.DO_NOTHING)

    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    mediosdepago = models.ForeignKey(MediosDePago, on_delete=models.DO_NOTHING, null=True)

    # Activa (estado inicial): la transacción permanece en este estado durante su ejecución.
    activa = 'AC'
    # Parcialmente Comprometida: la transacción pasa a este estado cuando acaba de realizar la última instrucción.
    parcial = 'PA'
    # Fallida: la transacción pasa a este estado tras descubrir que no puede continuar la ejecución normal.
    fallida = 'FA'
    # Abortada: la transacción pasa a este estado después de haber restablecido la base de datos a su estado anterior.
    abortada = 'AB'
    # Comprometida: la transacción pasa a este estado tras completarse con éxito.
    comprometida = 'CO'
    estado_tipos = [
        (activa, 'Activa'),
        (parcial, 'Parcialmente Comprometida'),
        (fallida, 'Fallida'),
        (abortada, 'Abortada'),
        (comprometida, 'Comprometida'),
    ]
    estado = models.CharField(max_length=2, choices=estado_tipos,default=activa)
    fecha_actu = models.DateTimeField(default=datetime.now, blank=True)
    fecha_crea = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.tocata.nombre
