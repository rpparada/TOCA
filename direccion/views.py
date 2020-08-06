from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url

from facturacion.models import FacturacionProfile

from .forms import DireccionForm

# Create your views here.
def checkout_direccion_create_view(request):
    form = DireccionForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():

        print(request.POST)
        instance = form.save(commit=False)
        fact_profile, fact_profile_created = FacturacionProfile.objects.new_or_get(request)
        if fact_profile is not None:
            tipo_direccion = request.POST.get('tipo_dir', 'envio')
            instance.facturacion_profile = fact_profile
            instance.tipo_direccion = tipo_direccion
            instance.save()
            request.session['direccion_'+tipo_direccion+'_id'] = instance.id
            print('direccion_'+tipo_direccion+'_id')
        else:
            print("Error aqui")
            return redirect('checkout')

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('checkout')

    return redirect('checkout')
