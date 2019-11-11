from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from apps.core.models import *
from apps.customer.models import *
from .forms import *
import datetime, datetime
from django.db.models import F
from django.db.models import Count, Sum
from django.db import connection
# Create your views here.

class HomecolaboratorView(TemplateView):
    template_name = "dashboard-collaborator.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        day = (today.weekday() + 6) % 7 #0 Dom #1 Lun #2 Mar...
        lastpay = today - datetime.timedelta(day)
        lastpay = datetime.datetime.combine(lastpay, datetime.time.min)  
        today = datetime.datetime.combine(today, datetime.time.max)  
        orders = Order.objects.filter(datetime_finally__range=(lastpay, today), service__colaborator=self.request.user, status='finalized').annotate(payColaborator=F('price') - F('utility'))
        newOrders = Order.objects.filter(service__colaborator=self.request.user, status='request').count()
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        todayOrders = Order.objects.filter(service__colaborator=self.request.user, datetime_booking__range=(today_min, today_max), status='ready').annotate(payColaborator=F('price') - F('utility')).count()
        with connection.cursor() as cursor:
            cursor.execute("select distinct(DATE(datetime_finally)),sum(price-utility) from customer_order where status='finalized' group by DATE(datetime_finally)")
            context["dataGraphic"] = cursor.fetchall()
        
        context["ordersThisWeek"] = orders
        context["countNewOrders"] = newOrders
        context["countTodayOrders"] = todayOrders
        context["time"] = datetime.datetime.now()
        return context

class OrdersColaboboratorView(ListView):
    def get_queryset(self, **kwargs):
        if 'filter' in self.request.GET:
            fil = self.request.GET.get('filter')
            if fil == 'news':
                queryset = Order.objects.filter(service__colaborator=self.request.user, status='request').annotate(payColaborator=F('price') - F('utility'))
            elif fil == 'today':
                today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
                queryset = Order.objects.filter(service__colaborator=self.request.user, datetime_booking__range=(today_min, today_max), status='ready').annotate(payColaborator=F('price') - F('utility'))
        else:
            queryset = Order.objects.filter(service__colaborator=self.request.user).order_by('status').annotate(payColaborator=F('price') - F('utility'))
        return queryset
    
    def get_context_data(self, **kwargs):
        statusOrders = {
            'request':'Solicitado',
            'accepted':'Aceptado',
            'waitpayment':'Esperando pago',
            'rejected':'Rechazado',
            'ready': 'Listo para iniciar',
            'expired':'Expirado',
            'inprogress':'Iniciado',
            'finalized':'Finalizado'
        }
        context = super().get_context_data(**kwargs)
        context["titleTable"] = "test"
        context["status"] = statusOrders
        context["time"] = datetime.datetime.now()
        return context
    
    def post(self, request, *args, **kwargs):
        order= get_object_or_404(Order, pk=request.POST.get('id'), service__colaborator=request.user)
        order.status = request.POST.get('status')
        order.save()
        return redirect(reverse('colaborator:orders'))

class ServicesColaboratorView(ListView):
    template_name = 'myservices.html'
    paginate_by = 2
    def get_queryset(self):
        queryset = ServicePerColaborator.objects.filter(colaborator=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        typePay = {
            'hours':'Horas',
            'full':'Tarifa unica',
        }
        context = super(ServicesColaboratorView, self).get_context_data(**kwargs)
        context["typePay"] = typePay
        context["time"] = datetime.datetime.now()
        return context

class CreateServiceColaboratorView(SuccessMessageMixin, CreateView):
    model = ServicePerColaborator
    form_class = ServicePerColaboratorForm
    template_name = 'createservicecolaborator.html'
    success_message = '¡Se ha asignado un nuevo servicio en su cuenta!'
    
    def get_success_url(self):
        return reverse('colaborator:myservices')

    def form_valid(self, form):
        form.instance.colaborator = self.request.user
        return super(CreateServiceColaboratorView, self).form_valid(form)