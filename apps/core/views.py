from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from .forms import *
from .models import *
from django.contrib import messages 
from django.urls import reverse_lazy, reverse
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
            #if user.password:
            #    user.set_password(user.password)
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
                          {'user_form':user_form,
                           'profile_form':profile_form})