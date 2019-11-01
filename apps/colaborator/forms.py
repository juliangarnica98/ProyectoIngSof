from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):

  username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
      'type': 'text',
      'placeholder': 'Nombre de usuario',
    }))
  password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
      'type': 'password',
      'placeholder': 'Password'
    }))

  def clean(self):
    user_found = User.objects.filter(username = self.cleaned_data['username']).exists()
    if not user_found:
      self.add_error('username', 'Username y/o password no encontrados')
    else:
      user = User.objects.get(username = self.cleaned_data['username'])
      if not user.check_password(self.cleaned_data['password']):
        self.add_error('username', 'Password incorrecto')