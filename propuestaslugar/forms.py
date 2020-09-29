from django import forms

from .models import LugaresTocata

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
