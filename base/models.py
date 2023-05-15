import os
from django.contrib.auth.models import User
from django.db import models

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=14, null=True)
    avatar = models.ImageField(upload_to='assets/images', null=True)
