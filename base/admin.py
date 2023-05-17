from django.contrib import admin
from .models import Product, Profile

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display = ('name', 'price', 'discount', 'stock', 'featured_image', 'created_by', 'created_at', 'updated_at')

class ProfileAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display = ('user', 'address', 'phone', 'role', 'avatar')

admin.site.register(Product,ProductAdmin)
admin.site.register(Profile, ProfileAdmin)