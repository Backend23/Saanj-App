# Generated by Django 5.1.2 on 2024-11-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saanj_app', '0020_order_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]
