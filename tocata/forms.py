from django import forms

from .models import Tocata, LugaresTocata, TocataAbierta
from lugar.models import Region, Comuna

class TocataForm(forms.ModelForm):

    class Meta:
        model = Tocata
        exclude = ('fecha_actu','fecha_crea','asistentes_total','evaluacion','asistentes_max','estado','region','comuna','usuario','artista')

class TocataAbiertaForm(forms.ModelForm):

    region = forms.ModelChoiceField(queryset=Region.objects, empty_label=None)
    comuna = forms.ModelChoiceField(queryset=Comuna.objects, empty_label=None)

    class Meta:
        model = TocataAbierta
        exclude = ('estado','fecha_actu','fecha_crea','artista','usuario')

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
