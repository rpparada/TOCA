from django import forms

class AgregaEmailAdicional(forms.Form):

    email           = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
                                                                "class": "form-control",
                                                                "placeholder": "Email",
                                                            }), label='Email'
                                    )
