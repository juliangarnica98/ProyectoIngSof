from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
  pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  pass
