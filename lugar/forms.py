from django import forms
from .models import Lugar, Region, Provincia, Comuna

class LugarForm(forms.ModelForm):

    nombre          = forms.CharField(widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre'
                                                            }), label='Nombre'
                                    )

    nombre_calle    = forms.CharField()
    numero          = forms.IntegerField()
    ciudad          = forms.CharField()
    departamento    = forms.CharField()
    otros           = forms.CharField()
    descripción     = forms.CharField()
    capacidad       = forms.IntegerField()

    region          = forms.ModelChoiceField(queryset=Region.objects, empty_label=None)
    comuna          = forms.ModelChoiceField(queryset=Comuna.objects, empty_label=None)

    class Meta:
        model       = Lugar
        exclude     = ['usuario','fecha_crea','fecha_actua','estado','codigo_postal','evaluacion','pais','provincia',]

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

class RegionForm(forms.ModelForm):

    class Meta:
        model = Region
        fields = '__all__'

class ComunaForm(forms.ModelForm):

    class Meta:
        model = Comuna
        fields = '__all__'

class ProvinciaForm(forms.ModelForm):

    class Meta:
        model = Provincia
        fields = '__all__'
