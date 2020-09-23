from django import forms
from django.contrib import messages

import datetime

from .models import Tocata
from lugar.models import Region, Comuna, Lugar
from artista.models import Artista

from toca.parametros import parToca

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class CrearTocataForm(forms.ModelForm):

    nombre              = forms.CharField(widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre'
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
    flayer_original     = forms.ImageField(required=False, widget=forms.FileInput(attrs={
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
            'flayer_original'
            )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CrearTocataForm, self).__init__(*args, **kwargs)
        self.fields['lugar'].queryset = Lugar.objects.filter(usuario=user).filter(estado=parToca['disponible'])

    def save(self, commit=True):
        tocata = super(CrearTocataForm, self).save(commit=False)

        if tocata.flayer_original:
            tocata.flayer_380_507 = tocata.flayer_original
            tocata.flayer_1920_1280 = tocata.flayer_original

        tocata.estado = 'publicado'
        tocata.region = tocata.lugar.region
        tocata.comuna = tocata.lugar.comuna

        tocata.usuario = self.user
        artista = Artista.objects.get(usuario=self.user)
        tocata.artista = artista
        tocata.asistentes_max = tocata.lugar.capacidad

        if commit:
            tocata.save()
            tocata.estilos.set(artista.estilos.all())
            #messages.success(request, 'Tocata creada exitosamente')

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
