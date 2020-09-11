from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from .utils import Mailchimp

# Create your models here.
user = settings.AUTH_USER_MODEL

class MarketingPreference(models.Model):
    user                    = models.OneToOneField(user, on_delete=models.CASCADE)
    subscribed              = models.BooleanField(default=True)
    mailchimp_msg           = models.TextField(null=True, blank=True)

    fecha_actu              = models.DateTimeField(auto_now=True)
    fecha_crea              = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

def make_marketing_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = Mailchimp().add_email(instance.user.email)
        print(status_code, response_data)

post_save.connect(make_marketing_create_receiver, sender=MarketingPreference)

def make_marketing_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed:
        status_code, response_data = Mailchimp().subscribed(instance.user.email)
        if response_data['status']:
            instance.subscribed = True
        else:
            instance.subscribed = False
    else:
        status_code, response_data = Mailchimp().unsubscribe(instance.user.email)

pre_save.connect(make_marketing_update_receiver, sender=MarketingPreference)


def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    if created:
        MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(make_marketing_pref_receiver, sender=user)
