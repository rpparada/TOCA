from django import forms

from .models import AnulacionEntrada

class MarcarComoEnviadaTBKForm(forms.Form):

    anulacion       = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(MarcarComoEnviadaTBKForm, self).__init__(*args, **kwargs)
        self.fields['anulacion'].queryset = AnulacionEntrada.objects.all()

class MarcarComoReembolsadoForm(forms.Form):

    anulacion       = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(MarcarComoReembolsadoForm, self).__init__(*args, **kwargs)
        self.fields['anulacion'].queryset = AnulacionEntrada.objects.all()

class MarcarComoReembolsadoTBKForm(forms.Form):

    anulacion       = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(MarcarComoReembolsadoTBKForm, self).__init__(*args, **kwargs)
        self.fields['anulacion'].queryset = AnulacionEntrada.objects.all()
