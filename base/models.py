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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='assets/images')

class Profile(models.Model):
    USER_ROLE = [
        ('Seller', 'SELLER'),
        ('Customer', 'CUSTOMER')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=14, default='')
    avatar = models.ImageField(upload_to='assets/images', null=True)
    role = models.CharField(choices=USER_ROLE, max_length=15, default='Customer')

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[Min(1)], default=1)

class Order(models.Model):
    ORDER_STATUS = [
        ('Pending', 'PENDING'),
        ('Delivered', 'DELIVERED'),
        ('Cancelled', 'CANCELLED')
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Plant, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(validators=[Min(1)], default=1)
    status = models.CharField(choices=ORDER_STATUS, max_length=15, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)