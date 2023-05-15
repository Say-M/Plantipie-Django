from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator as Min, MaxValueValidator as Max

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    price = models.FloatField(validators=[Min(0.0)])
    discount = models.FloatField(validators=[Min(0.0), Max(100.0)], default=0)
    stock = models.IntegerField(validators=[Min(0)], default=0)
    featured_image = models.ImageField(upload_to='assets/images')
    additional_images = models.ImageField(upload_to='assets/images', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Profile(models.Model):
    USER_ROLE = [
        ('Seller', 'SELLER'),
        ('Customer', 'CUSTOMER')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=14, null=True)
    avatar = models.ImageField(upload_to='assets/images', null=True)
    role = models.CharField(choices=USER_ROLE, max_length=15, default='customer')