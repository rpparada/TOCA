from __future__ import absolute_import, unicode_literals

import random
import time

from celery.decorators import task

from transaccional.models import EmailTemplate

from tocata.models import Tocata

@task(name='email_anulacion_tocata')
def email_anulacion_tocata(template_key, tocata_id, subject, sender, emails):

    tocata = Tocata.objects.get(id=tocata_id)

    EmailTemplate.send(
        template_key,
        context = { 'object': tocata },
        subject = subject,
        sender = sender,
        emails = emails
    )

    return None
