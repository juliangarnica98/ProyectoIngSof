from django import forms
from .models import Profile
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'Password','class':'form-control'}))
  confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={ 'placeholder': 'Repita su password', 'class':'form-control'}))
  class Meta():
      model = User
      fields = ('username','password','email', 'first_name','last_name')
      exclude = ['password']
      widgets = {
          'first_name': forms.TextInput(attrs={'placeholder': 'Nombre','class':'form-control'}),
          'last_name': forms.TextInput(attrs={'placeholder': 'Apellido','class':'form-control'}),
          'username': forms.TextInput(attrs={'placeholder': 'Username','class':'form-control'}),
          'email': forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control'}),
          'last_name': forms.EmailInput(attrs={'placeholder': 'Apellido','class':'form-control'}),
      }
  def __init__(self, *args, **kwargs):
      super(RegisterForm, self).__init__(*args, **kwargs)

  def clean(self):
      cleaned_data = super(RegisterForm, self).clean()
      password = cleaned_data.get("password")
      confirm_password = cleaned_data.get("confirm_password")
      if password != confirm_password:
        self.add_error('confirm_password', "Su contraseña no coincide")
class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username','password','email', 'first_name','last_name')
        exclude = ['password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombre','class':'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido','class':'form-control'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username','class':'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email','class':'form-control'}),
            'last_name': forms.EmailInput(attrs={'placeholder': 'Apellido','class':'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
          self.add_error('confirm_password', "Su contraseña no coincide")


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
      model = Profile
      fields = ('type_document','document', 'avatar', 'birth_date', 'city', 'location', 'mobile')
      exclude = ['user']
      widgets = {
        'type_document': forms.Select({'class':'form-control'}),
        'city': forms.Select({'class':'form-control'}),
        'location': forms.TextInput(attrs={'placeholder': 'Direccion','class':'form-control'}),
        'mobile': forms.NumberInput(attrs={'placeholder': 'Celular','class':'form-control'}),
        'document': forms.NumberInput(attrs={'placeholder': 'Documento','class':'form-control'}),
        'birth_date': forms.DateInput(attrs={'placeholder':'Fecha nacimiento', 'id':'datetimepicker1','class':'form-control'})
      }
    def __init__(self, *args, **kwargs):
        super(UserProfileInfoForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False