from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *


app_name = 'authenticate'

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('logout/', login_required(LogoutView.as_view()), name="logout"),
]