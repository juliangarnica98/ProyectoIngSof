from django import forms
from apps.core.models import *

class ServicePerColaboratorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ServicePerColaboratorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ServicePerColaborator
        exclude = ['colaborator']

        fields = ('coverage_city', 'rate_type', 'pet_types', 'rate', 'description', 'service')
        widgets = {
            'coverage_city': forms.Select(attrs={
                'placeholder': 'Ciudad de cobertura',
                'class':'form-control'
            }),
            'rate_type': forms.Select(attrs={
                'placeholder': 'Ciudad de cobertura',
                'class':'form-control'
            }),
            'pet_types': forms.CheckboxSelectMultiple(attrs={
                
            }),
            'rate': forms.TextInput(attrs={
                'type' : 'text',
                'placeholder': 'Tarifa',
                'class':'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class':'form-control',
                'placeholder': "Describa su servicio"
            }),
            'service': forms.Select(attrs={
                'placeholder': 'Servicio',
                'class':'form-control'
            }),
        }
        labels = {
            'coverage_city': "Ciudad de cobertura",
            'rate_type': "Tipo de cobro",
            'pet_types': "Tipo de mascota",
            'rate': "Tarifa",
            'description': "Descripción",
            'service': "Servicio",
        }