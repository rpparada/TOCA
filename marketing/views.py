from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, View
from django.http import HttpResponse
from django.contrib.messages.views import SuccessMessageMixin

from .models import MarketingPreference

from .forms import MarketingPreferenceForm

from .utils import Mailchimp

from .mixins import CsrfExemptMixin

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)

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

class MailchimpWebhookView(CsrfExemptMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Gracias', status=200)
        
    def post(self, request, *args, **kwargs):
        data = request.POST

        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            email = data.get('data[email]')
            hook_type = data.get('type')
            status_code, response_data = Mailchimp().change_subscription_status(email)
            sub_status = response_data['status']

            is_subbed = None
            mailchimp_subbed = None
            if sub_status == 'subscribed':
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == 'unsubscribed':
                is_subbed, mailchimp_subbed = (False, False)

            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                            subscribed=is_subbed,
                            mailchimp_subscribed=mailchimp_subbed,
                            mailchimp_msg=str(data)
                        )

        return HttpResponse('Gracias', status=200)
