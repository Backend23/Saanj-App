from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class SubCategory1(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SubCategory2(models.Model):
    name = models.CharField(max_length=100)
    subcategory1 = models.ForeignKey(SubCategory1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SubCategory3(models.Model):
    name = models.CharField(max_length=100)
    subcategory2 = models.ForeignKey(SubCategory2, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Design(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Allow null and blank
    image = models.ImageField(upload_to='designs/', null=True, blank=True)  # Added blank=True for consistency
    subcategory1 = models.ForeignKey(SubCategory1, on_delete=models.CASCADE, null=True, blank=True)
    subcategory2 = models.ForeignKey(SubCategory2, on_delete=models.CASCADE, null=True, blank=True)
    subcategory3 = models.ForeignKey(SubCategory3, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class DesignMedia(models.Model):
    design = models.ForeignKey(Design, related_name='media', on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='design_media/', null=True, blank=True)

    def __str__(self):
        return f'Media for {self.design.title}'

class DesignImage(models.Model):
    design = models.ForeignKey(Design, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='designs/images/', null=True, blank=True)

    def __str__(self):
        return f'Image for {self.design.title}'

class DesignVideo(models.Model):
    design = models.ForeignKey(Design, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='designs/videos/', null=True, blank=True)

    def __str__(self):
        return f'Video for {self.design.title}'
    
class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default="No description provided.")
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)  # Add QR code field

    def __str__(self):
        return self.name

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    shop_name = models.CharField(max_length=100, null=True, blank=True)
    shop_address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email_id = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    shop_logo = models.ImageField(upload_to='shop_logos/', null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    payment_status = models.BooleanField(default=False)  # Track payment completion

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.shop_name