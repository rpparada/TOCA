from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.
# Perfil usuarios
class PerfilUserQuerySet(models.query.QuerySet):
    def by_request(self, request):
        qs = self.filter(user=request.user)
        obj = None
        if qs.count() == 1:
            obj = qs.first()

        return obj

class PerfilUserManager(models.Manager):
    def get_queryset(self):
        return PerfilUserQuerySet(self.model, using=self._db)

    def create_perfiluser(self, user, nombre=None, apellido=None):
        perfil_obj = self.model(
            user = user,
            nombre = nombre,
            apellido = apellido
        )
        perfil_obj.save(using=self._db)
        return perfil_obj

    def by_request(self, request):
        return self.get_queryset().by_request(request)

class PerfilUser(models.Model):

    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre              = models.CharField(max_length=255, blank=True, null=True)
    apellido            = models.CharField(max_length=255, blank=True, null=True)

    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    objects             = PerfilUserManager()

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

# Perfil Artista
class PerfilArtistaManager(models.Manager):
    def create_perfilartista(self, user, rut, digitoVerificador, num_celular, banco, num_cuenta, tipo_cuenta):
        perfil_obj = self.model(
            user = user,
            rut = rut,
            digitoVerificador = digitoVerificador,
            num_celular = num_celular,
            banco = banco,
            num_cuenta = num_cuenta,
            tipo_cuenta = tipo_cuenta
        )
        perfil_obj.save(using=self._db)
        return perfil_obj

class PerfilArtista(models.Model):

    user                = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    rut                 = models.IntegerField(default=0)
    digitoVerificador   = models.CharField(max_length=1,default='0')
    num_celular         = models.CharField(max_length=50, default=0)
    banco               = models.CharField(max_length=200, choices=BANCOS_OPCIONES,default='012')
    num_cuenta          = models.CharField(max_length=100)
    tipo_cuenta         = models.CharField(max_length=200, choices=TIPOS_CUENTAS_OPCIONES,default='001')

    objects             = PerfilArtistaManager()

    def __str__(self):
        return 'Artista '+self.user.email
