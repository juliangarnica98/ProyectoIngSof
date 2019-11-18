from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib import messages 
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User, Group
# Create your views here.

class HomeView(TemplateView):
    template_name = "welcome.html"

class MyProfile(View):
    def get(self, request):
        profile = Profile.objects.filter(user=request.user)
        if profile.exists():
            profile = profile[0]
            profile_form = UserProfileInfoForm(instance=profile)
        else:
            profile_form = UserProfileInfoForm()
        user_form = UserForm(instance=request.user)
        return render(request,'profile.html',
                          { 'user_form':user_form,
                            'titleUser':'Mi perfil',
                            'filebase': 'colaborator/base.html',
                            'backform': 'colaborator:home',
                            'profile': profile,
                            'profile_form':profile_form})

    def post(self, request):
        profile = Profile.objects.filter(user=request.user)
        if profile.exists():
            profile = profile[0]
        user_form = UserForm(data=request.POST,instance=request.user)
        profile_form = UserProfileInfoForm(data=request.POST, files=request.FILES or None,instance=profile or None)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            profile.save()
            messages.add_message(request, messages.SUCCESS, "Datos almacenados con éxito.")
            return redirect(reverse('core:myprofile'))
        else:
            return render(request,'profile.html',
                          { 'user_form':user_form,
                            'titleUser':'Mi perfil',
                            'filebase': 'colaborator/base.html',
                            'backform': 'colaborator:home',
                            'profile_form':profile_form})

class NewProfile(View):
    def get(self,request, *args, **kwargs):
        user_form = RegisterForm()
        profile_form = UserProfileInfoForm()
        titleUser = 'Colaboradores' if kwargs['typeuser'] == 'collaborators' else 'Cliente'
        return render(request,'profile.html',
                          { 'user_form':user_form,
                            'titleUser':titleUser,
                            'filebase': 'base.html',
                            'backform': 'core:home',
                            'profile_form':profile_form})

    def post(self,request, *args, **kwargs):
        user_form = RegisterForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST, files=request.FILES or None)
        titleUser = 'Colaboradores' if kwargs['typeuser'] == 'collaborators' else 'Cliente'
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.save()
            group = Group.objects.get(name=kwargs['typeuser'])
            user.groups.add(group)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
            profile.save()
            messages.add_message(request, messages.SUCCESS, "Se ha registrado ahora puede autenticarse.")
            return redirect(reverse('authenticate:login'))
        else:
            return render(request,'profile.html',
                          { 'user_form':user_form,
                            'titleUser':titleUser,
                            'filebase': 'base.html',
                            'backform': 'core:home',
                            'profile_form':profile_form})
