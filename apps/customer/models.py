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

    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_ORDER = [
        ('request', 'Solicitado'),
        ('accepted', 'Aceptado'),
        ('waitpayment', 'Esperando pago'),
        ('rejected', 'Rechazado'),
        ('expired', 'Expirado'),
        ('ready', 'Listo para iniciar'),
        ('inprogress', 'Iniciado'),
        ('revertPay', 'Declinado, reversar pago'),
        ('finalized', 'Finalizado')
    ]
    price = models.PositiveIntegerField()
    utility = models.PositiveIntegerField(default=0, editable=False)
    datetime_booking = models.DateTimeField()
    datetime_finally = models.DateTimeField()
    status = models.CharField(max_length=255, blank=False, choices=STATUS_ORDER)
    score = models.FloatField(blank=True, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    service = models.ForeignKey(ServicePerColaborator, on_delete=models.CASCADE, default=1)
    is_payment = models.BooleanField(blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)

    def calculate_utility(self):
        if self.status == 'finalized':
            return int(self.price * 0.15)
        else:
            return 0

    def save(self,*args,**kwargs):
        self.utility = self.calculate_utility()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Num order %s" % (self.pk)