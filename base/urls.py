from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product', views.product, name='product'),
    path('product/<str:id>/', views.product_detail, name='product_detail'),
    path('checkout', views.checkout, name='checkout'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
]