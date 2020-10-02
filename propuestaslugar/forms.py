from django import forms
from django.contrib import messages

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
                                        queryset=None,
                                        empty_label=None,
                                        widget=forms.HiddenInput()
                                    )

    lugar               = forms.ModelChoiceField(
                                        queryset=None,
                                        empty_label=None,
                                        # widget=forms.Select(attrs={
                                        #                     'class': 'form-control',
                                        #                 }),
                                        widget=forms.RadioSelect(attrs={'class': "custom-radio-list"}),
                                        label='Selecciona lugar:'
                                    )

    def __init__(self, request, tocataabierta, *args, **kwargs):
        self.request = request
        super(ProponerLugarForm, self).__init__(*args, **kwargs)

        lugares = Lugar.objects.none()
        tocataabierta_qs = TocataAbierta.objects.none()
        if tocataabierta:
            tocataabierta_qs = TocataAbierta.objects.filter(id=tocataabierta.id)
            if tocataabierta.comuna.nombre == 'Todas':
                # Buscar por region
                lugares = Lugar.objects.by_region(tocataabierta, request)
            else:
                # Buscar por comuna
                lugares = Lugar.objects.by_comuna(tocataabierta, request)

        self.fields['lugar'].queryset = lugares
        self.fields['tocataabierta'].queryset = tocataabierta_qs
        self.fields['lugar'].initial = lugares.first()

    def clean_lugar(self):
        request = self.request
        lugar = self.cleaned_data.get('lugar')
        tocataabierta = self.cleaned_data.get('tocataabierta')
        if tocataabierta.comuna.nombre == 'Todas':
            if tocataabierta.region.nombre != lugar.region.nombre:
                messages.error(request,'Lugar no esta en la Region')
                raise forms.ValidationError('Lugar no esta en la Region')
        else:
            if tocataabierta.region.nombre != lugar.region.nombre or tocataabierta.comuna.nombre != lugar.comuna.nombre:
                messages.error(request,'Lugar no esta en la Region y/o Comuna')
                raise forms.ValidationError('Lugar no esta en la Region y/o Comuna')

        return lugar
