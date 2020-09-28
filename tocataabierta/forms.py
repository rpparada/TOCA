from django import forms
from django.utils import timezone
from datetime import timedelta

from .models import TocataAbierta
from lugar.models import Region, Comuna, Lugar
from artista.models import Artista

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class CrearTocataAbiertaForm(forms.ModelForm):

    nombre              = forms.CharField(widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre',
                                                                'autofocus': True
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
    flayer_380_507      = forms.ImageField(required=False, widget=forms.FileInput(attrs={
                                                                'class': 'form-control-file',
                                                            }), label='Subir Flayer'
                                        )

    class Meta:
        model = TocataAbierta
        fields = (
            'nombre',
            'region',
            'comuna',
            'descripción',
            'fecha',
            'hora',
            'asistentes_min',
            'flayer_380_507'
        )

    def __init__(self, request, *args, **kwargs):
        self.request = request
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

    def clean_asistentes_min(self):
        asistentes_min = self.cleaned_data.get('asistentes_min')
        # Asistentes minimos debe ser mayor a 0
        if asistentes_min <= 0:
            raise forms.ValidationError('Debes definir un minimo de asistentes mayor a cero')

        return asistentes_min

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        # La fecha de las tocatas deben definirce con una semana de anticipacion
        if (fecha - timezone.now().date()) <= timedelta(days=5):
            raise forms.ValidationError('Debes definir una fecha futura con al menos 7 dias de anticipacion')

        return fecha

    def save(self, commit=True):
        tocataabierta = super(CrearTocataAbiertaForm, self).save(commit=False)
        request = self.request

        tocataabierta.usuario = request.user
        artista = Artista.objects.get(usuario=request.user)
        tocataabierta.artista = artista

        if commit:
            tocataabierta.save()
            tocataabierta.estilos.set(artista.estilos.all())

        return tocataabierta

class SuspenderTocataAbiertaForm(forms.Form):

    tocataabierta       = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(SuspenderTocataAbiertaForm, self).__init__(*args, **kwargs)
        self.fields['tocataabierta'].queryset = TocataAbierta.objects.tocataartista_by_request(self.request)

class BorrarTocataAbiertaForm(forms.Form):

    tocataabierta       = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BorrarTocataAbiertaForm, self).__init__(*args, **kwargs)
        self.fields['tocataabierta'].queryset = TocataAbierta.objects.tocataartista_by_request(self.request)
