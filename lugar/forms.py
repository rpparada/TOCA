from django import forms
from .models import Lugar, Region, Provincia, Comuna

class CrearLugarForm(forms.ModelForm):

    nombre          = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre',
                                                                'autofocus': True
                                                            }), label='Nombre'
                                    )

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
    descripción     = forms.CharField(required=False, widget=forms.Textarea(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Descripción'
                                                            }), label='Descripción'
                                    )
    capacidad       = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Capacidad'
                                                            }), label='Capacidad Aprox.'
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
        model = Lugar
        exclude = [
                'usuario',
                'fecha_crea',
                'fecha_actua',
                'estado',
                'codigo_postal',
                'evaluacion',
                'pais',
                'provincia',
            ]

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

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        # Numero calle debe ser mayor a 0
        if numero <= 0:
            raise forms.ValidationError('Numero calle debe ser mayor a cero')

        return numero

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        # Capacidad debe ser mayor a 0
        if capacidad <= 0:
            raise forms.ValidationError('Capacidad debe ser mayor a cero')

        return capacidad

    def save(self, commit=True):
        lugar = super(CrearLugarForm, self).save(commit=False)
        request = self.request

        lugar.provincia = Comuna.objects.get(id=lugar.comuna.id).provincia
        lugar.usuario = request.user

        if commit:
            lugar.save()

        return lugar

class ActualizaLugarForm(forms.Form):

    lugar           = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    descripción     = forms.CharField(required=False, widget=forms.Textarea(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Descripción'
                                                            }), label='Descripción'
                                    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ActualizaLugarForm, self).__init__(*args, **kwargs)
        self.fields['lugar'].queryset = Lugar.objects.by_request(self.request)

class BorrarLugarForm(forms.Form):

    lugar           = forms.ModelChoiceField(queryset=None,
                                empty_label=None,
                                widget=forms.HiddenInput()
                            )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(BorrarLugarForm, self).__init__(*args, **kwargs)
        self.fields['lugar'].queryset = Lugar.objects.by_request(self.request)

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

class CrearLugarPropuestaForm(forms.ModelForm):

    nombre          = forms.CharField(required=False, widget=forms.TextInput(attrs={
                                                                'id': 'primercampo',
                                                                'class': 'form-control',
                                                                'placeholder': 'Nombre',
                                                                'autofocus': True
                                                            }), label='Nombre'
                                    )

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
    descripción     = forms.CharField(required=False, widget=forms.Textarea(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Descripción'
                                                            }), label='Descripción'
                                    )
    capacidad       = forms.IntegerField(widget=forms.NumberInput(attrs={
                                                                'class': 'form-control',
                                                                'placeholder': 'Capacidad'
                                                            }), label='Capacidad Aprox.'
                                    )

    region          = forms.ModelChoiceField(queryset=None,
                                                empty_label=None,
                                                widget=forms.Select(attrs={
                                                                    'class': 'form-control',
                                                                    'id': 'xx_region'
                                                                        }
                                        ), label='Region'
                                    )
    comuna          = forms.ModelChoiceField(queryset=Comuna.objects,
                                                empty_label=None,
                                                widget=forms.Select(attrs={
                                                                    'class': 'form-control',
                                                                    'id': 'xx_comuna'
                                                                        }
                                        ), label='Comuna'
                                    )

    class Meta:
        model = Lugar
        exclude = [
                'usuario',
                'fecha_crea',
                'fecha_actua',
                'estado',
                'codigo_postal',
                'evaluacion',
                'pais',
                'provincia',
            ]

    def __init__(self, request, tocataabierta, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['region'].queryset = Region.objects.filter(id=tocataabierta.region.id)
        if tocataabierta.comuna.nombre == 'Todas':
            self.fields['comuna'].queryset = Comuna.objects.filter(region=tocataabierta.region)
        else:
            self.fields['comuna'].queryset = Comuna.objects.filter(id=tocataabierta.comuna.id)

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        # Numero calle debe ser mayor a 0
        if numero <= 0:
            raise forms.ValidationError('Numero calle debe ser mayor a cero')

        return numero

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        # Capacidad debe ser mayor a 0
        if capacidad <= 0:
            raise forms.ValidationError('Capacidad debe ser mayor a cero')

        return capacidad

    def save(self, commit=True):
        lugar = super(CrearLugarForm, self).save(commit=False)
        request = self.request

        lugar.provincia = Comuna.objects.get(id=lugar.comuna.id).provincia
        lugar.usuario = request.user

        if commit:
            lugar.save()

        return lugar
