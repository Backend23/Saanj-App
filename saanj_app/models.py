from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings

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
    
class Package(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default="No description provided.")
    qr_code = models.ImageField(upload_to='qrcodes/', null=True, blank=True)
    level = models.IntegerField(default=1)  # Add a level to indicate package hierarchy

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
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='designs', null=True)

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
    



class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    shop_name = models.CharField(max_length=100, null=True, blank=True)
    shop_address = models.TextField(null=True, blank=True)  # This remains for the shop's address
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email_id = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    shop_logo = models.ImageField(upload_to='shop_logos/', null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)
    payment_status = models.BooleanField(default=False)  # Track payment completion

    @property
    def default_address(self):
        return self.addresses.filter(is_default=True).first() or self.shop_address


    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.shop_name
    
# Address model to store multiple addresses for each vendor
class Address(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='addresses')
    shop_number = models.CharField(max_length=50, null=True, blank=True)  # Shop number/building number
    street = models.CharField(max_length=100, null=True, blank=True)  # Street
    area = models.CharField(max_length=100, null=True, blank=True)  # Area
    city = models.CharField(max_length=50, null=True, blank=True)  # City
    state = models.CharField(max_length=50, null=True, blank=True)  # State
    pincode = models.CharField(max_length=10, null=True, blank=True)  # Pincode
    is_default = models.BooleanField(default=False)

    def full_address(self):
        # Combine all parts of the address into a single string
        return f"{self.shop_number}, {self.street}, {self.area}, {self.city}, {self.state}, {self.pincode}"

    def save(self, *args, **kwargs):
        # Ensure only one default address per vendor
        if self.is_default:
            Address.objects.filter(vendor=self.vendor).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_address()

# Order model to handle design orders by vendors
class Order(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=[('Placed', 'Placed'), ('In Making', 'In Making'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], default='placed')  # Or whatever status you prefer
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Failed', 'Failed')], default='Paid')

    def __str__(self):
        return f"Order {self.id} by {self.vendor.shop_name} for {self.design.title}"