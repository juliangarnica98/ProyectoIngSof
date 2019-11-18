# Generated by Django 2.2.6 on 2019-11-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_auto_20191118_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('request', 'Solicitado'), ('waitpayment', 'Esperando pago'), ('rejected', 'Rechazado'), ('cancelled', 'Cancelado'), ('ready', 'Listo para iniciar'), ('inprogress', 'Iniciado'), ('revertPay', 'Declinado, reversar pago'), ('finalized', 'Finalizado')], max_length=255),
        ),
    ]
