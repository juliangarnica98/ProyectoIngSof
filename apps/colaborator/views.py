from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
# Create your views here.

class HomecolaboratorView(TemplateView):
    template_name = "dashboard-collaborator.html"
