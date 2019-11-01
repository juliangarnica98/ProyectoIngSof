from django.db import models

# Create your models here.

class Colaborator(models.Model):
    idPerson   = models.IntegerField()
    name = models.CharField(max_length=50)
    mail = models.EmailField()
    experience = models.TextField()
    phone = models.CharField(max_length=12)
    address = models.TextField()
    qualification = models.IntegerField(default=5)
    date_of_birth = models.DateField()                    
