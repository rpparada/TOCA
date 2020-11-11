from datetime import timedelta
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

from django.db.models import Q
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.utils import timezone
from django.urls import reverse

from transaccional.models import EmailTemplate

from toca.utils import random_string_generator, unique_key_generator

import celery

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 7)

DEBUG = getattr(settings, 'DEBUG', True)
# Create your models here.

#User
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, nombre=None, apellido=None, is_active=True, is_staff=False, is_admin=False, is_musico=False):
        if not email:
            raise ValueError("Nuevo usuario debe tener email")
        if not password:
            raise ValueError("Nuevo usuario debe tener contreña")

        user_obj = self.model(
            email = self.normalize_email(email),
            nombre = nombre,
            apellido = apellido
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.musico = is_musico
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None, nombre=None, apellido=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None, nombre=None, apellido=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

    def create_musico(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_musico=True
        )
        return user

class User(AbstractBaseUser):

    email           = models.EmailField(max_length=255, unique=True)
    nombre          = models.CharField(max_length=255, blank=True, null=True)
    apellido        = models.CharField(max_length=255, blank=True, null=True)
    is_active       = models.BooleanField(default=True)
    staff           = models.BooleanField(default=False)
    admin           = models.BooleanField(default=False)

    musico          = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'

    REQUIRED_FIELDs = []

    objects         = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.nombre and self.apellido:
            return self.nombre+' '+self.apellido
        return seld.email

    def get_short_name(self):
        if self.nombre:
            return self.nombre
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_musico(self):
        return self.musico

# Email Activacion
class EmailActivationQuerySet(models.query.QuerySet):
    def confirmable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated = False,
            forced_expired = False
        ).filter(
            fecha_crea__gt=start_range,
            fecha_crea__lt=end_range
        )

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self, email):
        return self.get_queryset().filter(
                Q(email=email) |
                Q(user__email=email)
            ).filter(
                activated=False
            )

class EmailActivation(models.Model):
    user                = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    email               = models.EmailField()
    key                 = models.CharField(max_length=120, blank=True, null=True)
    activated           = models.BooleanField(default=False)
    forced_expired      = models.BooleanField(default=False)
    expires             = models.IntegerField(default=7) # Dias

    fecha_crea          = models.DateTimeField(auto_now_add=True)
    fecha_actua         = models.DateTimeField(auto_now=True)

    objects             = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.is_active = True
            user.save()
            self.activated = True
            self.save()

            recipient_list = [self.email]
            if DEBUG:
                recipient_list = ['rpparada@gmail.com']

            # Enviar Email con celery
            celery.current_app.send_task('bienvenido_nuevo_usuario',(
                    'bienvenido_nuevo_usuario',
                    self.email,
                    'Bienvenido a Tocatas Íntimas',
                    recipient_list
            ))

            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL', '127.0.0.1:8000')
                key_path = reverse('cuenta:email-activate', kwargs={'key':self.key})
                path = '{base}{path}'.format(base=base_url,path=key_path)
                recipient_list = [self.email]

                if DEBUG:
                    recipient_list = ['rpparada@gmail.com']

                # Enviar Email con celery
                celery.current_app.send_task('validacion_email',(
                        'validacion_email',
                        path,
                        self.email,
                        '1-Click Verificacion de Email',
                        recipient_list
                ))

                return True
        return False

def pre_save_email_validation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_validation, sender=EmailActivation)

def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        if instance.is_musico:
            obj.activated = True
            obj.save()
        else:
            obj.send_activation()

post_save.connect(post_save_user_create_receiver, sender=User)
