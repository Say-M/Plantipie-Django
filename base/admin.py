from django.contrib import admin
from .models import Product, Profile, AdditionalImage, Cart, Order, OrderProduct

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

class CartAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display=('user','product','quantity')

class OrderAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display=('user','status','created_at','updated_at')

class OrderProductAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display=('product','quantity','price','discount')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(AdditionalImage, AdditionalImageAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)