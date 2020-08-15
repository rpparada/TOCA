from django import forms

from .models import TocataAbierta
from lugar.models import Region, Comuna, Lugar

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

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
