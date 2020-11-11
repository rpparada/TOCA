from __future__ import absolute_import, unicode_literals

import random
import time

from celery.decorators import task

from transaccional.models import EmailTemplate

from tocata.models import Tocata
from anulaciones.models import TocataCancelada

@task(name='email_anulacion_tocata')
def email_anulacion_tocata(template_key, tocata_id, subject, emails):

    tocata = Tocata.objects.get(id=tocata_id)
    context = {
        'object': tocata,
    }

    EmailTemplate.send(
        template_key,
        context = context,
        subject = subject,
        emails = emails
    )

    return None

@task(name='email_anulacion_tocata_artista')
def email_anulacion_tocata_artista(template_key, tocata_cancelada_id, subject, emails):

    tocata_cancelada = TocataCancelada.objects.get(id=tocata_cancelada_id)

    context = {
        'object': tocata_cancelada,
    }

    EmailTemplate.send(
        template_key,
        context = context,
        subject = subject,
        emails = emails
    )

    return None

@task(name='validacion_email')
def validacion_email(template_key, path, email, subject, emails):

    context = {
        'path': path,
        'email': email
    }

    EmailTemplate.send(
        template_key,
        context = context,
        subject = subject,
        emails = emails
    )

    return None

@task(name='formulario_nuevo_artista')
def formulario_nuevo_artista(template_key, domain, uid, token, subject, emails):

    context = {
        'domain': domain,
        'uid': uid,
        'token': token
    }

    EmailTemplate.send(
        template_key,
        context = context,
        subject = subject,
        emails = emails
    )

    return None

@task(name='bienvenido_nuevo_usuario')
def bienvenido_nuevo_usuario(template_key, email, subject, emails):

    context = {
        'email': email
    }

    EmailTemplate.send(
        template_key,
        context = context,
        subject = subject,
        emails = emails
    )

    return None
