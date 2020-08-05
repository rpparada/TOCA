from django import forms

from .models import Direccion
from lugar.models import Region, Comuna

class DireccionForm(forms.ModelForm):

    nombre_calle    = forms.CharField(widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre Calle'
                                                            }), label='Calle'
                                    )

    numero          = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Número Calle'
                                                            }), label='Número'
                                    )
    ciudad          = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Ciudad'
                                                            }), label='Ciudad'
                                    )
    departamento    = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Departamento'
                                                            }), label='Depto.'
                                    )
    otros           = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Block/Villa/etc.'
                                                            }), label='Otros'
                                    )

    region          = forms.ModelChoiceField(queryset=Region.objects, empty_label=None, widget=forms.Select(attrs={
                                                                                        'class': 'form-control',
                                                                                        'id': 'id_region'
                                                            }), label='Region'
                                    )
    comuna          = forms.ModelChoiceField(queryset=Comuna.objects, empty_label=None, widget=forms.Select(attrs={
                                                                                        'class': 'form-control',
                                                                                        'id': 'id_comuna'
                                                            }), label='Comuna'
                                    )

    class Meta:
        model = Direccion
        exclude = ['facturacion_profile',
                    'tipo_direccion',
                    'pais',
                    'codigo_postal'
                    ]

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
