from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.
# Perfil usuarios
class PerfilUser(models.Model):

    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre              = models.CharField(max_length=255, blank=True, null=True)
    apellido            = models.CharField(max_length=255, blank=True, null=True)

    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

# Perfil Artistas
BANCOS_OPCIONES = (
    ('012','BANCO DEL ESTADO DE CHILE'),
    ('001','BANCO DE CHILE'),
    ('009','BANCO INTERNACIONAL'),
    ('014','SCOTIABANK CHILE'),
    ('016','BANCO DE CREDITO E INVERSIONES'),
    ('028','BANCO BICE'),
    ('031','HSBC BANK (CHILE)'),
    ('037','BANCO SANTANDER-CHILE'),
    ('039','ITAÚ CORPBANCA'),
    ('049','BANCO SECURITY'),
    ('051','BANCO FALABELLA'),
    ('053','BANCO RIPLEY'),
    ('055','BANCO CONSORCIO'),
    ('504','SCOTIABANK AZUL (ex BANCO BILBAO VIZCAYA ARGENTARIA, CHILE (BBVA))'),
    ('059','BANCO BTG PACTUAL CHILE'),
)

TIPOS_CUENTAS_OPCIONES = (
    ('001','Cuenta Corriente'),
    ('002','Cuenta de Ahorro'),
    ('003','Cuenta Vista'),
    ('004','Cuenta Chequera Electrónica'),
    ('005','Cuenta RUT'),
)

class PerfilArtista(models.Model):

    user                = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    rut                 = models.IntegerField(default=0)
    digitoVerificador   = models.CharField(max_length=1,default='0')
    num_celular         = models.CharField(max_length=50, default=0)
    banco               = models.CharField(max_length=200, choices=BANCOS_OPCIONES,default='012')
    num_cuenta          = models.CharField(max_length=100)
    tipo_cuenta         = models.CharField(max_length=200, choices=TIPOS_CUENTAS_OPCIONES,default='001')

    def __str__(self):
        return 'Artista '+self.user.email
