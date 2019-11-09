from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(TypePet)
class TypePetAdmin(admin.ModelAdmin):
  pass

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
  pass

@admin.register(ServicePerColaborator)
class ServicePerColaboratorAdmin(admin.ModelAdmin):
  pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  pass
