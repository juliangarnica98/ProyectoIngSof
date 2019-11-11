from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *


app_name = 'customer'

urlpatterns = [
    path('', HomeCustomer.as_view(), name="home"),
]