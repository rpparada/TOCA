from __future__ import absolute_import, unicode_literals

import random
import time

from celery.decorators import task

from transaccional.models import EmailTemplate

from tocata.models import Tocata

@task(name='email_anulacion_tocata')
def email_anulacion_tocata(template_key, tocata_id, subject, sender, emails):

    tocata = Tocata.objects.get(id=tocata_id)
    context = {
        'object': tocata,
    }

    EmailTemplate.send(
        template_key,
        context = context,
        subject = subject,
        sender = sender,
        emails = emails
    )

    return None

@task(name='validacion_email')
def validacion_email(template_key, path, email, subject, sender, emails):

    context = {
        'path': path,
        'email': email
    }

    EmailTemplate.send(
        template_key,
        context = context,
        subject = subject,
        sender = sender,
        emails = emails
    )

    return None
