from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('product/', views.productPage, name='product'),
    path('product/<str:id>/', views.productDetailPage, name='product_detail'),
    path('checkout/', views.checkoutPage, name='checkout'),
    path('login/', views.loginPage, name='login'),
    path('signup/', views.signupPage, name='signup'),
    path('logout/',views.logoutUser, name='logout'),
    path('profile/',views.profilePage, name='profile'),
    path('orders/',views.orderPage, name='orders'),
]