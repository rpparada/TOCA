from django import forms
from .models import Lugar, Region, Provincia, Comuna

class LugarForm(forms.ModelForm):

    '''
    Referencia implementacion:
    https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html
    '''

    region = forms.ModelChoiceField(queryset=Region.objects, empty_label=None)
    comuna = forms.ModelChoiceField(queryset=Comuna.objects, empty_label=None)

    class Meta:
        model = Lugar
        exclude = ['nombre','usuario','fecha_crea','fecha_actua','estado','codigo_postal','evaluacion','pais','provincia',]

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
