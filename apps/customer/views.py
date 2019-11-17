from django.shortcuts import render
from django.views.generic import FormView, TemplateView, RedirectView, View
from .models import *

# Create your views here.

class HomeCustomer(TemplateView):
    template_name = "mis-mascotas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pets'] = Pet.objects.filter(owner = self.request.user)
        return context