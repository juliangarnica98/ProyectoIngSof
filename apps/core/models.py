from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class TypePet(models.Model):
    PET_TYPE = [
        ('domestico', 'Domestico'),
        ('exotico', 'Exotico'),
        ('salvaje', 'Salvaje')
    ]
    PET_CATEGORIES = [
        ('mamifero', 'Mamífero'),
        ('ave', 'Ave'),
        ('pez', 'Pez'),
        ('reptil', 'Reptil'),
        ('invertebrado', 'Invertebrado'),
        ('anfibio', 'Anfibio')
    ]
    name = models.CharField(max_length=255, blank=True, null=True)
    petType = models.CharField(max_length=255, blank=False, choices=PET_TYPE, default='domestico')
    category = models.CharField(max_length=255, blank=False, choices=PET_CATEGORIES, default='mamifero')
    
    def __str__(self):
        return self.name
        
class Service(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    pet_types = models.ManyToManyField(TypePet)
    colaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ServicePerColaborator', related_name='colaborators')

    def __str__(self):
        return self.name

class ServicePerColaborator(models.Model):
    CITIES = [
        ('Bogota', 'Bogotá'),
        ('Medellin', 'Medellín'),
        ('Cali', 'Calí'),
        ('Barranquilla', 'Barranquilla'),
    ]
    RATE_TYPE = [
        ('hours', 'Horas'),
        ('full', 'Tarifa unica'),
    ]
    coverage_city = models.CharField(max_length=255, blank=False, choices=CITIES, default='Bogota')
    rate_type = models.CharField(max_length=255, blank=False, choices=RATE_TYPE, default='hours')
    rate = models.PositiveIntegerField()
    description = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    colaborator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['service', 'colaborator'], name='colaborator_x_service')
        ]

    def __str__(self):
        return "Proveedor: %s Servicio:%s" % (self.colaborator,self.service)

class Profile(models.Model):
    DOC_TYPES = [
        ('cc', 'Cedula de ciudadania'),
        ('ti', 'Tarjeta de identidad'),
        ('ce', 'Cedula extranjeria'),
        ('passport', 'Pasaporte'),
    ]
    CITIES = [
        ('Bogota', 'Bogotá'),
        ('Medellin', 'Medellín'),
        ('Cali', 'Calí'),
        ('Barranquilla', 'Barranquilla'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type_document = models.CharField(max_length=255, blank=False, choices=DOC_TYPES, default='cc')
    document = models.CharField(max_length=25, blank=False)
    avatar = models.ImageField(upload_to='profile/')
    birth_date = models.DateField(null=True, blank=False)
    city = models.CharField(max_length=255, blank=False, choices=CITIES, default='Bogota')
    location = models.CharField(max_length=255, blank=False)
    mobile = models.CharField(max_length=10, blank=False)
    