from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.views.generic import FormView, TemplateView, RedirectView

# Authentication imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy, reverse



class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "authenticate/login.html"

    def dispatch(self, request, *args, **kwargs):
        if  not request.user.is_anonymous:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get('next') 
        return context

    def get_success_url(self):
        nextPage = self.request.POST.get('next')
        if str(nextPage) != "None":
            return nextPage
        else:
            return reverse_lazy("colaborator:home")
            
class LogoutView(RedirectView):
    pattern_name = 'core:home'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
