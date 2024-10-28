# Generated by Django 5.1.2 on 2024-10-25 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saanj_app', '0010_paymentpackage_vendor_active_package'),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='active_package',
        ),
        migrations.AddField(
            model_name='vendor',
            name='package',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='saanj_app.package'),
        ),
        migrations.DeleteModel(
            name='PaymentPackage',
        ),
    ]
