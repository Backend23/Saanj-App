# Generated by Django 5.1.2 on 2024-10-25 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saanj_app', '0012_vendor_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='description',
            field=models.TextField(default='No description provided.'),
        ),
        migrations.AddField(
            model_name='package',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/'),
        ),
        migrations.AlterField(
            model_name='package',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]