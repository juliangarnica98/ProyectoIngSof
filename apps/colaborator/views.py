from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .forms import LoginForm

class HomecolaboratorView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

class RegisterColaborador(View):
    def get(self, request,*args, **kwargs):
        form = LoginForm
        return render(request,'registerColaborator.html', {'form':form})
