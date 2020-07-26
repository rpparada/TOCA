from django import forms

import datetime

from .models import Tocata, LugaresTocata, TocataAbierta
from lugar.models import Region, Comuna, Lugar

from toca.parametros import parToca

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class TocataForm(forms.ModelForm):

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
        exclude = ('fecha_actu',
                    'fecha_crea',
                    'asistentes_total',
                    'evaluacion',
                    'asistentes_max',
                    'estado',
                    'region',
                    'comuna',
                    'usuario',
                    'artista',
                    'flayer_1920_1280',
                    'flayer_380_507',
                    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TocataForm, self).__init__(*args, **kwargs)

        self.fields['lugar'].queryset = Lugar.objects.filter(usuario=user).filter(estado=parToca['disponible'])


class TocataAbiertaForm(forms.ModelForm):

    nombre              = forms.CharField(widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre'
                                                            }), label='Nombre'
                                        )
    region              = forms.ModelChoiceField(queryset=Region.objects, empty_label=None, widget=forms.Select(attrs={
                                                                                        'class': 'form-control',
                                                                                        'id': 'opcionesregion'
                                                            }), label='Region'
                                        )
    comuna              = forms.ModelChoiceField(queryset=Comuna.objects, empty_label=None, widget=forms.Select(attrs={
                                                                                        'class': 'form-control',
                                                                                        'id': 'opcionescomuna'
                                                            }), label='Comuna'
                                        )
    descripción         = forms.CharField(required=False, widget=forms.Textarea(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Descripción'
                                                            }), label='Descripción'
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
        model = TocataAbierta
        exclude = ('estado',
                    'fecha_actu',
                    'fecha_crea',
                    'artista',
                    'usuario',
                    'flayer_1920_1280',
                    'flayer_380_507',
                    'costo',
                    'tocata')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comuna'].queryset = Comuna.objects.none()

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['comuna'].queryset = self.instance.region.comuna_set.order_by('nombre')

class LugaresTocataForm(forms.ModelForm):

    class Meta:
        model = LugaresTocata
        exclude = ('fecha_actu','fecha_crea','estado')
