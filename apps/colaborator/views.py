from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from apps.core.models import *
from apps.customer.models import *
from .forms import *
import datetime, datetime
from django.db.models import F
from django.db.models import Count, Sum
from django.db import connection
from django.core.exceptions import ValidationError
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
            queryToGraph = """select distinct(DATE(customer_order.datetime_finally)),sum(customer_order.price-customer_order.utility) 
                                from customer_order inner join core_servicepercolaborator on customer_order.service_id = core_servicepercolaborator.id 
                                where customer_order.status='finalized' 
                                and core_servicepercolaborator.colaborator_id = %s
                                group by DATE(customer_order.datetime_finally)
                                order by date ASC""" % self.request.user.id
            cursor.execute(queryToGraph)
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
                queryset = Order.objects.filter(service__colaborator=self.request.user, datetime_booking__range=(today_min, today_max)).annotate(payColaborator=F('price') - F('utility')).order_by('id')
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
            'revertPay': 'Declinado, reversar pago',
            'finalized':'Finalizado'
        }
        context = super().get_context_data(**kwargs)
        context["titleTable"] = "test"
        context["status"] = statusOrders
        context["time"] = datetime.datetime.now()
        return context
    
    def post(self, request, *args, **kwargs):
        queryget = ""
        if 'filter' in self.request.GET:
            queryget = "?filter=%s" % self.request.GET.get('filter')       

        order= get_object_or_404(Order, pk=request.POST.get('id'), service__colaborator=request.user)
        order.status = request.POST.get('status')
        if order.status == 'finalized':
            order.datetime_finally = datetime.datetime.now()
        order.save()
        return redirect(reverse('colaborator:orders') + queryget)

class ServicesColaboratorView(ListView):
    template_name = 'myservices.html'
    paginate_by = 15
    def get_queryset(self):
        queryset = ServicePerColaborator.objects.filter(colaborator=self.request.user).order_by('id')
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
    template_name = 'servicecolaborator.html'
    success_message = '¡Se ha asignado un nuevo servicio en su cuenta!'
    
    def get_success_url(self):
        return reverse('colaborator:myservices')
    
    def get_context_data(self, **kwargs):
        context = super(CreateServiceColaboratorView, self).get_context_data(**kwargs)
        context["time"] = datetime.datetime.now()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.colaborator = self.request.user

        try:
            self.object.full_clean()
        except ValidationError:
            #raise ValidationError("No can do, you have used this name before!")
            #return self.form_invalid(form)
            form._errors["service"] = "Este servicio ya esta siendo prestado por ud. por favor edite su actual servicio."
            return super(CreateServiceColaboratorView, self).form_invalid(form)
        return super(CreateServiceColaboratorView, self).form_valid(form)
    
class UpdateServiceColaboratorView(UpdateView):
    model = ServicePerColaborator
    form_class = ServicePerColaboratorForm
    template_name = 'servicecolaborator.html'
    success_message = '¡Se ha actualizado el servicio en su cuenta!'
    
    def get_success_url(self):
        return reverse('colaborator:myservices')

class DeleteServiceColaboratorView(DeleteView):
    model = ServicePerColaborator
    
    def get(self, request, pk):
        service = get_object_or_404(ServicePerColaborator, pk=pk)
        service.delete()
        return redirect(reverse('colaborator:myservices'))