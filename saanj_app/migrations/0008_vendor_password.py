# Generated by Django 5.1.2 on 2024-10-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saanj_app', '0007_remove_vendor_password_alter_design_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
