# Generated by Django 5.1.2 on 2024-10-18 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saanj_app', '0003_vendor_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]