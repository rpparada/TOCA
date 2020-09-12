from django.urls import path
from . import views

urlpatterns = [
    path('conf/email', views.MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    path('webhook/mailchimp', views.MailchimpWebhookView.as_view(), name='webhook-mailchimp'),
]
