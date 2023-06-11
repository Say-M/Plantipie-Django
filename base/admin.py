from django.contrib import admin
from .models import Product, Profile, AdditionalImage

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display = ('name', 'price', 'discount', 'stock', 'featured_image', 'created_by', 'created_at', 'updated_at')

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display = ('user', 'address', 'phone', 'role', 'avatar')

class AdditionalImageAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display = ('product', 'image')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(AdditionalImage, AdditionalImageAdmin)
