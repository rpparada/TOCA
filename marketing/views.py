from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin

from .models import MarketingPreference

from .forms import MarketingPreferenceForm

# Create your views here.

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'marketing/marketing-pref.html'
    success_url = '/marketing/conf/email'
    success_message = 'Cambios actualizados'


    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/cuenta/ingresar?next=/marketing/conf/email')

        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self):
        user = self.request.user
        obj, created = MarketingPreference.objects.get_or_create(user=user)

        return obj
