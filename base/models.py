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

    def discount_price(self):
        return self.price - ((self.price * self.discount) / 100)


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
    
def carts(self):
    return Cart.objects.filter(user=self)
User.add_to_class('carts', carts)

def cart_count(self):
    return Cart.objects.filter(user=self).count()
User.add_to_class('cart_count', cart_count)

def total_cart_price(self):
    total = 0
    carts = Cart.objects.filter(user=self)
    for cart in carts:
        total += cart.total()
    return total
User.add_to_class('total_cart_price', total_cart_price)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[Min(1)], default=1)

    def total(self):
        return (self.quantity * self.product.price) - ((self.quantity * self.product.price * self.product.discount) / 100)

class Order(models.Model):
    ORDER_STATUS = [
        ('Pending', 'PENDING'),
        ('Delivered', 'DELIVERED'),
        ('Canceled', 'CANCELED')
    ]
    PAYMENT_METHOD = [
        ('Cash On Delivery', 'Cash On Delivery'),
        ('BKash', 'BKash'),
        ('Nagad', 'Nagad'),
    ]
    
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=14, null=True)
    billing_address = models.TextField(max_length=300, null=True)
    shipping_address = models.TextField(max_length=300, null=True)
    payment_method = models.CharField(max_length=15, null=True)
    transaction_id = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=ORDER_STATUS, max_length=15, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def products(self):
        return OrderProduct.objects.filter(order=self)
    
    def total(self):
        total = 0
        order_products = OrderProduct.objects.filter(order=self)
        for order_product in order_products:
            total += order_product.discount_price()
        return total

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[Min(1)], default=1)
    price = models.FloatField(validators=[Min(0.0)])
    discount = models.FloatField(validators=[Min(0.0), Max(100.0)], default=0)

    def total(self):
        return self.quantity * self.price

    def discount_price(self):
        return (self.quantity * self.price) - ((self.quantity * self.price * self.discount) / 100)