from django import forms

from .models import LugaresTocata

from tocataabierta.models import TocataAbierta
from lugar.models import Lugar

class LugaresTocataForm(forms.ModelForm):

    class Meta:
        model = LugaresTocata
        exclude = ('fecha_actu','fecha_crea','estado')

class CancelarPropuestaForm(forms.Form):

    propuesta           = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CancelarPropuestaForm, self).__init__(*args, **kwargs)
        self.fields['propuesta'].queryset = LugaresTocata.objects.mis_propuestas_by_request(self.request)

class BorrarPropuestaForm(forms.Form):

    propuesta           = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BorrarPropuestaForm, self).__init__(*args, **kwargs)
        self.fields['propuesta'].queryset = LugaresTocata.objects.para_borrar_by_request(self.request)

class CancelarPropuestaElegidaForm(forms.Form):

    propuesta           = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(CancelarPropuestaElegidaForm, self).__init__(*args, **kwargs)
        self.fields['propuesta'].queryset = LugaresTocata.objects.elegidas_by_request(self.request)

class ProponerLugarForm(forms.Form):

    tocataabierta       = forms.ModelChoiceField(
                                        queryset=TocataAbierta.objects.disponible(),
                                        empty_label=None,
                                        widget=forms.HiddenInput()
                                    )

    lugar               = forms.ModelChoiceField(
                                        queryset=None,
                                        empty_label=None,
                                        widget=forms.Select(attrs={
                                                            'class': 'form-control',
                                                        }),
                                        label='Selecciona lugar:'
                                    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ProponerLugarForm, self).__init__(*args, **kwargs)
        self.fields['lugar'].queryset = Lugar.objects.by_request(self.request)
