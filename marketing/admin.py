from django.contrib import admin

from .models import MarketingPreference
# Register your models here.

class MarketingPreferenceAdmin(admin.ModelAdmin):
    list_display = ['__str__','subscribed','fecha_actu']
    readonly_fields = ['mailchimp_msg','mailchimp_subscribed','fecha_actu','fecha_crea']

    class Meta:
        model = MarketingPreference
        fields = [
            'user',
            'subscribed',
            'mailchimp_msg',
            'mailchimp_subscribed',
            'fecha_actu',
            'fecha_crea',
        ]

admin.site.register(MarketingPreference, MarketingPreferenceAdmin)
