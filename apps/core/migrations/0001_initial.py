# Generated by Django 2.2.6 on 2019-11-09 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TypePet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('petType', models.CharField(choices=[('domestico', 'Domestico'), ('exotico', 'Exotico'), ('salvaje', 'Salvaje')], default='domestico', max_length=255)),
                ('category', models.CharField(choices=[('mamifero', 'Mamífero'), ('ave', 'Ave'), ('pez', 'Pez'), ('reptil', 'Reptil'), ('invertebrado', 'Invertebrado'), ('anfibio', 'Anfibio')], default='mamifero', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ServicePerColaborator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coverage_city', models.CharField(choices=[('Bogota', 'Bogotá'), ('Medellin', 'Medellín'), ('Cali', 'Calí'), ('Barranquilla', 'Barranquilla')], default='Bogota', max_length=255)),
                ('rate_type', models.CharField(choices=[('hours', 'Horas'), ('full', 'Tarifa unica')], default='hours', max_length=255)),
                ('rate', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('colaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Service')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='colaborators',
            field=models.ManyToManyField(related_name='colaborators', through='core.ServicePerColaborator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='service',
            name='pet_types',
            field=models.ManyToManyField(to='core.TypePet'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_document', models.CharField(choices=[('cc', 'Cedula de ciudadania'), ('ti', 'Tarjeta de identidad'), ('ce', 'Cedula extranjeria'), ('passport', 'Pasaporte')], default='cc', max_length=255)),
                ('document', models.CharField(max_length=25)),
                ('avatar', models.ImageField(upload_to='profile/')),
                ('birth_date', models.DateField(null=True)),
                ('city', models.CharField(choices=[('Bogota', 'Bogotá'), ('Medellin', 'Medellín'), ('Cali', 'Calí'), ('Barranquilla', 'Barranquilla')], default='Bogota', max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
