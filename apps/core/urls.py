from django.urls import path
from .views import *


app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('myprofile', MyProfile.as_view(), name="myprofile"),
]