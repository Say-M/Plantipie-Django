from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator as Min, MaxValueValidator as Max

# Create your models here.
class Plant(models.Model):
    plant_name = models.CharField(max_length=255)
    discount = models.IntegerField()
    current_price = models.IntegerField()
    stock_count = models.IntegerField()
    description = models.TextField()
    featured_image = models.FileField(upload_to='assets/images',null=True)
    additional_image = models.FileField(upload_to='assets/images', null=True)

    def __str__(self):
        return self.plant_name

class AdditionalImage(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='assets/images',null=True)

    def __str__(self):
        return self.plant.plant_name
    

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