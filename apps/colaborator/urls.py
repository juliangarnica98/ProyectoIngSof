from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *


app_name = 'colaborator'

urlpatterns = [
    path('', login_required(HomecolaboratorView.as_view()), name="home"),
    path('orders', login_required(OrdersColaboboratorView.as_view()), name="orders"),
    path('myservices', login_required(ServicesColaboratorView.as_view()), name="myservices"),
    path('assingservice', login_required(CreateServiceColaboratorView.as_view()), name="assingservice")
]