from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name

class MetalType(models.Model):
    name = models.CharField(max_length=255)
    purity = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name

class WeightOption(models.Model):
    name = models.CharField(max_length=255)
    min_weight = models.DecimalField(max_digits=5, decimal_places=0)
    max_weight = models.DecimalField(max_digits=5, decimal_places=0)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')

    def __str__(self):
        return self.name
    

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    weight = models.FloatField()
    status = models.CharField(max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')
    image_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(Category)
    subcategories = models.ManyToManyField(Subcategory)
    metal_type = models.ForeignKey(MetalType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
