from django import forms
from apps.core.models import *

class ServicePerColaboratorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(ServicePerColaboratorForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ServicePerColaborator
        exclude = ['colaborator']

        