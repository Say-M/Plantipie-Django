from django.contrib import admin
from .models import Product, Profile, AdditionalImage

# Register your models here.
class PlantAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields=('id',)

class AdditionalImageAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display = ('product', 'image')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(AdditionalImage, AdditionalImageAdmin)

admin.site.register(AdditionalImage)