from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *

app_name = 'colaborator'

urlpatterns = [
   path('', login_required(HomecolaboratorView.as_view()), name="home"),
   path('registerColaborador/', RegisterColaborador.as_view(), name="registerCola"),    
]