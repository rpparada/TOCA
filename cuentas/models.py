from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

# Create your models here.
#User
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, nombre=None, apellido=None, is_active=True, is_staff=False, is_admin=False):
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
        user_obj.active = is_active
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

class User(AbstractBaseUser):

    email           = models.EmailField(max_length=255, unique=True)
    nombre          = models.CharField(max_length=255, blank=True, null=True)
    apellido        = models.CharField(max_length=255, blank=True, null=True)
    active          = models.BooleanField(default=True)
    staff           = models.BooleanField(default=False)
    admin           = models.BooleanField(default=False)

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
    def is_active(self):
        return self.active