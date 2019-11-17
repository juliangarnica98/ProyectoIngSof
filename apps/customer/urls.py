from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *


app_name = 'customer'

urlpatterns = [
    path('', HomeCustomer.as_view(), name="home"),
    path('createpet', CreatePetView.as_view(), name="createpet"),
    path('udpatepet/<int:pk>', UpdatePetView.as_view(), name="updatepet"),
    path('deletepet/<int:pk>', DeletePetView.as_view(), name="deletepet"),
    path('contractService/<int:pk>', ContractServiceView.as_view(), name="contractservice"),
]