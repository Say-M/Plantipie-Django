from django.db import models
# Create your models here.
class Plant(models.Model):
    cover_photo = models.ImageField(upload_to='base/static/assets/images')
    detail_photo_1 = models.ImageField(upload_to='base/static/assets/images')
    detail_photo_2 = models.ImageField(upload_to='base/static/assets/images')
    detail_photo_3 = models.ImageField(upload_to='base/static/assets/images')
    plant_name = models.CharField(max_length=255)
    previous_price = models.IntegerField()
    current_price = models.IntegerField()
    stock_count = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.plant_name