from django.db import models
from django.conf import settings
from apps.core.models import *
# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=255)
    edad = models.PositiveSmallIntegerField()
    pet_image = models.ImageField(upload_to='pets/')
    pet_type = models.ForeignKey(TypePet, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Order(models.Model):
    STATUS_ORDER = [
        ('request', 'Solicitado'),
        ('accepted', 'Aceptado'),
        ('waitpayment', 'Esperando pago'),
        ('rejected', 'Rechazado'),
        ('inprogress', 'Iniciado'),
        ('finalized', 'Finalizado')
    ]
    price = models.PositiveIntegerField()
    datetime_booking = models.DateTimeField()
    datetime_finally = models.DateTimeField()
    status = models.CharField(max_length=255, blank=False, choices=STATUS_ORDER)
    score = models.PositiveSmallIntegerField()
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    is_payment = models.BooleanField(blank=True, null=True)
    payment_date = models.DateTimeField()

    def __str__(self):
        return self.pk