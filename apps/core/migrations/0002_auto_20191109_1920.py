# Generated by Django 2.2.6 on 2019-11-10 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepercolaborator',
            name='rate',
            field=models.FloatField(),
        ),
    ]
