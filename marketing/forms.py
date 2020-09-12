from django import forms

from .models import MarketingPreference

class MarketingPreferenceForm(forms.ModelForm):

    subscribed              = forms.BooleanField(label='¿Quieres recibir email de marketing?', required=False)

    class Meta:
        model = MarketingPreference
        fields = [
            'subscribed'
        ]
