# Generated by Django 2.2.6 on 2019-11-18 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0009_order_hours_contract'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('request', 'Solicitado'), ('waitpayment', 'Esperando pago'), ('rejected', 'Rechazado'), ('expired', 'Expirado'), ('ready', 'Listo para iniciar'), ('inprogress', 'Iniciado'), ('revertPay', 'Declinado, reversar pago'), ('finalized', 'Finalizado')], max_length=255),
        ),
    ]