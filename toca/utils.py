import random
import string
import os
import tbk

from django.utils.text import slugify
from django.conf import settings

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):

    size = random.randint(30,45)
    key = random_string_generator(size=size)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key

def unique_orden_id_generator(instance, new_slug=None):

    orden_new_id = random_string_generator().upper()
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(orden_id=orden_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return orden_new_id

def unique_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.nombre)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

# Transbank conexion inicial (parametrizado para pruebas)
def inicia_transaccion(orden):
    transaction = webpay_service.init_transaction(
        amount=orden.total,
        buy_order=orden.orden_id,
        # Es la mejor opcion? Investigar
        return_url='http://' + settings.BASE_URL + '/carro/retornotbk',
        final_url='http://' + settings.BASE_URL + '/carro/compraexitosa',
        session_id=orden.facturacion_profile.id
    )
    return transaction

def retorna_transaccion(token):
    trans = webpay_service.get_transaction_result(token)
    trans_detail = trans["detailOutput"][0]

    return trans, trans_detail

def confirmar_transaccion(token):
    webpay_service.acknowledge_transaction(token)


CERTIFICATES_DIR = os.path.join('orden', "commerces")
NORMAL_COMMERCE_CODE = "597020000540"

def load_commerce_data(commerce_code):
    with open(
        os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + ".key"), "r"
    ) as file:
        key_data = file.read()
    with open(
        os.path.join(CERTIFICATES_DIR, commerce_code, commerce_code + ".crt"), "r"
    ) as file:
        cert_data = file.read()
    with open(os.path.join(CERTIFICATES_DIR, "tbk.pem"), "r") as file:
        tbk_cert_data = file.read()

    return {
        'key_data': key_data,
        'cert_data': cert_data,
        'tbk_cert_data': tbk_cert_data,
    }

normal_commerce_data = load_commerce_data(NORMAL_COMMERCE_CODE)
normal_commerce = tbk.commerce.Commerce(
    commerce_code=NORMAL_COMMERCE_CODE,
    key_data=normal_commerce_data['key_data'],
    cert_data=normal_commerce_data['cert_data'],
    tbk_cert_data=normal_commerce_data['tbk_cert_data'],
    environment=tbk.environments.DEVELOPMENT,
)
webpay_service = tbk.services.WebpayService(normal_commerce)

# Render to PDF para Boleta y Entrada
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
