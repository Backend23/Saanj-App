# Generated by Django 5.1.2 on 2024-11-06 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saanj_app', '0023_remove_order_status_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Failed', 'Failed')], default='Paid', max_length=20),
        ),
    ]