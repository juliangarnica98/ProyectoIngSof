from django import forms
from .models import Pet, Order

class PetForm(forms.ModelForm):
    class Meta():
        model = Pet
        fields = ('name','edad','pet_image', 'pet_type')
        exclude = ['owner']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nombre','class':'form-control'}),
            'edad': forms.NumberInput(attrs={'placeholder': 'Edad','class':'form-control'}),
            'pet_type': forms.Select(attrs={'class':'form-control'}),
        }
        labels = {
            'name': "Nombre",
            'edad': "Edad",
            'pet_type': "Tipo de mascota"
        }

class OrderForm(forms.ModelForm):
    class Meta():
        model = Order
        fields = ('datetime_booking','hours_contract')
        widgets = {
            'datetime_booking': forms.DateInput(attrs={'placeholder': 'Fecha de contratacion','class':'form-control booking'}),
            'hours_contract': forms.NumberInput(attrs={'placeholder': 'Horas a contratar','class':'form-control hours_contract'}),
        }
        labels = {
            'datetime_booking': "Fecha agendamiento",
            'hours_contract': "Horas de contratación",
        }