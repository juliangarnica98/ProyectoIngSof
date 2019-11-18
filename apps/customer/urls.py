from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *


app_name = 'customer'

urlpatterns = [
    path('', login_required(HomeCustomer.as_view()), name="home"),
    path('createpet', login_required(CreatePetView.as_view()), name="createpet"),
    path('udpatepet/<int:pk>', login_required(UpdatePetView.as_view()), name="updatepet"),
    path('deletepet/<int:pk>', login_required(DeletePetView.as_view()), name="deletepet"),
    path('contractService/<int:pk>', login_required(ContractServiceView.as_view()), name="contractservice"),
    path('myorders', login_required(MyOrdersView.as_view()), name="myorders"),
    path('generate-bill/<int:order>', login_required(GenerateBillView.as_view()), name="generatebill"),
]