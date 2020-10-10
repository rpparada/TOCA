from django import forms
from django.contrib import messages
from django.utils import timezone

from datetime import timedelta, datetime

from .models import Tocata
from lugar.models import Region, Comuna, Lugar
from artista.models import Artista
from tocataabierta.models import TocataAbierta
from propuestaslugar.models import LugaresTocata

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class CrearTocataForm(forms.ModelForm):

    nombre              = forms.CharField(widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre',
                                                                'autofocus': True
                                                            }), label='Nombre'
                                        )
    lugar               = forms.ModelChoiceField(queryset=None, empty_label=None, widget=forms.Select(attrs={
                                                                                        'class': 'form-control',
                                                            }), label='Mis Lugares'
                                    )
    descripción         = forms.CharField(required=False, widget=forms.Textarea(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Descripción'
                                                            }), label='Descripción'
                                        )
    costo               = forms.DecimalField(widget=forms.NumberInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Costo Adhesion'
                                                            }), label='Costo Adhesion'
                                        )
    fecha               = forms.DateField(widget=DateInput(attrs={
                                                                'class': 'form-control',
                                                            }), label='Fecha'
                                        )
    hora                = forms.TimeField(widget=TimeInput(attrs={
                                                                'class': 'form-control',
                                                            }), label='Hora'
                                        )
    asistentes_min      = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Asistentes Minimos'
                                                            }), label='Asistentes Mínimos'
                                        )
    flayer_380_507      = forms.ImageField(required=False, widget=forms.FileInput(attrs={
                                                                'class': 'form-control-file',
                                                            }), label='Subir Flayer'
                                        )

    class Meta:
        model = Tocata
        fields = (
            'nombre',
            'lugar',
            'descripción',
            'costo',
            'fecha',
            'hora',
            'asistentes_min',
            'flayer_380_507'
            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CrearTocataForm, self).__init__(*args, **kwargs)
        self.fields['lugar'].queryset = Lugar.objects.filter(usuario=request.user).filter(estado='disponible')

    def clean_costo(self):
        costo = self.cleaned_data.get('costo')
        # Costo de adhesion debe ser mayor a 0
        if costo <= 0:
            raise forms.ValidationError('Adhesion debe ser mayor a cero')

        return costo

    def clean_asistentes_min(self):
        asistentes_min = self.cleaned_data.get('asistentes_min')
        lugar = self.cleaned_data.get('lugar')
        # Asistentes minimos debe ser mayor a 0
        if asistentes_min <= 0:
            raise forms.ValidationError('Debes definir un minimo de asistentes mayor a cero')

        # Asistentes minimos no deben superar la capcidad del lugar seleccionado
        if asistentes_min > lugar.capacidad:
            raise forms.ValidationError('Lugar tiene una capacidad menor que el minimo de asistentes')

        return asistentes_min

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        # La fecha de las tocatas deben definirce con una semana de anticipacion
        if (fecha - timezone.now().date()) <= timedelta(days=5):
            raise forms.ValidationError('Debes definir una fecha futura con al menos 7 dias de anticipacion')

        return fecha

    def save(self, commit=True):
        tocata = super(CrearTocataForm, self).save(commit=False)
        request = self.request

        tocata.region = tocata.lugar.region
        tocata.comuna = tocata.lugar.comuna

        tocata.usuario = request.user
        artista = Artista.objects.get(usuario=request.user)
        tocata.artista = artista
        tocata.asistentes_max = tocata.lugar.capacidad

        if commit:
            tocata.save()
            tocata.estilos.set(artista.estilos.all())

        return tocata

class SuspenderTocataForm(forms.Form):

    tocata              = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(SuspenderTocataForm, self).__init__(*args, **kwargs)
        self.fields['tocata'].queryset = Tocata.objects.tocataartista_by_request(self.request)

class BorrarTocataForm(forms.Form):

    tocata              = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BorrarTocataForm, self).__init__(*args, **kwargs)
        self.fields['tocata'].queryset = Tocata.objects.tocataartista_by_request(self.request)

class TocataDesdeTocataAbiertaCreateForm(forms.ModelForm):

    nombre              = forms.CharField(widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre',
                                                                'readonly': True
                                                            }), label='Nombre'
                                        )
    lugar               = forms.ModelChoiceField(queryset=None, empty_label=None, widget=forms.Select(attrs={
                                                                                        'class': 'form-control',
                                                                                        'readonly': True
                                                            }), label='Mis Lugares'
                                    )
    descripción         = forms.CharField(required=False, widget=forms.Textarea(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Descripción',
                                                                'readonly': True,
                                                            }), label='Descripción'
                                        )
    costo               = forms.DecimalField(widget=forms.NumberInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Costo Adhesion',
                                                                'autofocus': True
                                                            }), label='Costo Adhesion'
                                        )
    fecha               = forms.DateField(widget=DateInput(attrs={
                                                                'class': 'form-control',
                                                                'readonly': True,
                                                            }), label='Fecha'
                                        )
    hora                = forms.TimeField(widget=TimeInput(attrs={
                                                                'class': 'form-control',
                                                                'readonly': True,
                                                            }), label='Hora'
                                        )
    asistentes_min      = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Asistentes Minimos',
                                                                'readonly': True,
                                                            }), label='Asistentes Mínimos'
                                        )
    tocataabierta       = forms.ModelChoiceField(queryset=None, empty_label=None, widget=forms.Select(attrs={
                                                                                        'class': 'form-control',
                                                                                        'readonly': True
                                                            }), label='Mis Lugares'
                                    )
    flayer_380_507      = forms.ImageField(required=False, widget=forms.FileInput(attrs={
                                                                'class': 'form-control-file',
                                                            }), label='Subir Flayer'
                                        )

    class Meta:
        model = Tocata
        fields = (
            'nombre',
            'lugar',
            'descripción',
            'costo',
            'fecha',
            'hora',
            'asistentes_min'
            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(TocataDesdeTocataAbiertaCreateForm, self).__init__(*args, **kwargs)
        lugar_id = request.POST.get('lugar')
        tocataabierta_id = request.POST.get('tocataabierta')

        self.fields['lugar'].queryset = Lugar.objects.filter(id=lugar_id)
        self.fields['tocataabierta'].queryset = TocataAbierta.objects.filter(id=tocataabierta_id)

    def clean_costo(self):
        costo = self.cleaned_data.get('costo')
        # Costo de adhesion debe ser mayor a 0
        if costo <= 0:
            raise forms.ValidationError('Ingresa precio de entrada')

        return costo

    def save(self, commit=True):
        tocata = super(TocataDesdeTocataAbiertaCreateForm, self).save(commit=False)
        request = self.request

        tocataabierta_id = request.POST.get('tocataabierta')
        tocataabierta = TocataAbierta.objects.get(id=tocataabierta_id)

        # Actualizar estado de tocata abierta
        tocataabierta.confirmar()

        # Actualizar estado de propuestas
        lugar_propuesto = LugaresTocata.objects.existe(tocataabierta, tocata.lugar)
        lugar_propuesto.elegir()
        lista_lugares = LugaresTocata.objects.filter(tocataabierta=tocataabierta).filter(estado='pendiente')
        for lugar in lista_lugares:
            lugar.no_elegir()

        # Agregar informacion restante a modelo Tocata
        # Definir capacidad
        tocata.asistentes_max = tocata.lugar.capacidad
        if tocata.lugar.capacidad < tocata.asistentes_min:
            tocata.asistentes_min = tocata.lugar.capacidad

        tocata.flayer_380_507 = tocataabierta.flayer_380_507

        tocata.region = tocata.lugar.region
        tocata.comuna = tocata.lugar.comuna

        tocata.usuario = request.user

        artista = Artista.objects.get(usuario=request.user)
        tocata.artista = artista

        if commit:
            tocata.save()
            tocata.estilos.set(artista.estilos.all())

            # Asignar tocata a tocata intima
            tocataabierta.tocata = tocata
            tocataabierta.save()

        return tocata
