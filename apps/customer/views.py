from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, TemplateView, RedirectView, View, CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse
from .models import *
from apps.core.models import *
from .forms import *
from django.core.exceptions import ValidationError
from django.contrib import messages 
import datetime, datetime
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
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
        return render(request,'contract.html',{'object_list':queryset, 'typePay':typePay, 'formcontact':OrderForm, 'pet':pet})
    
    def post(self, request, *args, **kwargs):
        service = get_object_or_404(ServicePerColaborator, pk=request.POST.get('id_service'))
        pet = get_object_or_404(Pet, pk=request.POST.get('id_pet'))
        newOrder = Order(datetime_booking=request.POST.get('datetime_booking'), status="request", pet=pet, service=service)
        if service.rate_type == 'full':
            newOrder.price = service.rate
        else:
            newOrder.hours_contract = int(request.POST.get('hours_contract'))
            newOrder.price = service.rate * int(request.POST.get('hours_contract'))
        newOrder.save()
        messages.add_message(request, messages.SUCCESS, "Orden creada exitosamente, si desea ver su estado Mis ordenes brindara toda la información.")
        return redirect(reverse('customer:contractservice', kwargs={'pk': pet.id}))

class MyOrdersView(View):
    def get(self, request, *args, **kwargs):
        ordersPerType = []
        for key, value in Order.STATUS_ORDER: 
            if key == 'request':
                headers = ['#','Servicio','Agendada','Precio','Mascota','Acciones']
                spanactions = 1
            if key == 'waitpayment':
                headers = ['#','Servicio','Agendada','Precio','Mascota','Acciones']
                spanactions = 2
            if key == 'cancelled':
                headers = ['#','Servicio','Agendada','Precio','Mascota']
                spanactions = 0
            if key == 'rejected':
                headers = ['#','Servicio','Mascota']
                spanactions = 0
            if key == 'ready':
                headers = ['#','Servicio','Agendada','Mascota', 'Acciones']
                spanactions = 2
            if key == 'inprogress':
                headers = ['#','Servicio','Agendada','Mascota']
                spanactions = 2
            if key == 'revertPay':
                headers = ['#','Servicio','Mascota']
                spanactions = 2
            if key == 'finalized':
                headers = ['#','Servicio','Agendada','Precio','Mascota','Acciones','Puntua']
                spanactions = 2
            orders = {
                'status': key,
                'legend': value,
                'headers': headers,
                'spanactions': spanactions,
                'orders': Order.objects.filter(status=key, pet__owner=request.user).order_by('id')
            }
            ordersPerType.append(orders)
        context = {'orderstype':ordersPerType}
        return render(request,'customer/myorders.html',context)
    
    def post(self, request, *args, **kwargs):
        order= get_object_or_404(Order, pk=request.POST.get('id'), pet__owner=request.user)
        order.status = request.POST.get('status')
        print(request.POST)
        if order.status == 'ready':
            order.is_payment = True
            order.payment_date = datetime.datetime.now()

        if order.status == 'finalized':
            print(request.POST.get('rating%s' % order.id))
            order.score = request.POST.get('rating%s' % order.id)
            order.datetime_finally = datetime.datetime.now()
        order.save()
        return redirect(reverse('customer:myorders'))

class GenerateBillView(View):
    def get(self, request, *args, **kwargs):
        order= get_object_or_404(Order, pk=kwargs['order'], pet__owner=request.user)
        w, h = letter
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)
        text = p.beginText(50, h - 50)
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        text.textLine("Factura # %s"% kwargs['order'])
        text.textLine("Servicio: %s" % order.service.service.name)
        text.textLine("Mascota: %s" % order.pet.name)
        text.textLine("Fecha de servicio: %s" % order.datetime_booking)
        text.textLine("Fecha de servicio: %s" % order.datetime_booking)
        text.textLine("Fecha de pago: %s" % order.payment_date)
        text.textLine("Precio: %s" % order.price)
        text.textLine("Pagado por: %s %s" % (order.pet.owner.first_name,order.pet.owner.last_name))
        p.drawText(text)
        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='factura%s.pdf' % kwargs['order'])