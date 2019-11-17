from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, TemplateView, RedirectView, View, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse
from .models import *
from apps.core.models import *
from .forms import *
from django.core.exceptions import ValidationError
# Create your views here.

class HomeCustomer(TemplateView):
    template_name = "mis-mascotas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pets'] = Pet.objects.filter(owner = self.request.user)
        return context

class CreatePetView(CreateView):
    model = Pet
    form_class=PetForm
    template_name = 'petmanage.html'
    
    def get_success_url(self):
        return reverse('customer:home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user

        try:
            self.object.full_clean()
        except ValidationError:
            return super(CreatePetView, self).form_invalid(form)
        return super(CreatePetView, self).form_valid(form)

class UpdatePetView(UpdateView):
    model = Pet
    form_class=PetForm
    template_name = 'petmanage.html'
    
    def get_success_url(self):
        return reverse('customer:home')


class DeletePetView(DeleteView):
    model = Pet
    
    def get(self, request, pk):
        service = get_object_or_404(Pet, pk=pk)
        service.delete()
        return redirect(reverse('customer:home'))

class ContractServiceView(View):
    def get(self, request, *args, **kwargs):
        typePay = {
            'hours':'Horas',
            'full':'Tarifa unica',
        }
        pet = get_object_or_404(Pet, pk=kwargs['pk'])
        queryset = ServicePerColaborator.objects.filter(pet_types=pet.pet_type)
        return render(request,'contract.html',{'object_list':queryset, 'typePay':typePay, 'formcontact':OrderForm})
    