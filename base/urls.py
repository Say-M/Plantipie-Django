from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homePage, name='home'),
    path('product/', views.productPage, name='product'),
    path('product/<str:id>/', views.productDetailPage, name='product_detail'),
    path('checkout/', views.checkoutPage, name='checkout'),
    path('login/', views.loginPage, name='login'),
    path('signup/', views.signupPage, name='signup'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profilePage, name='profile'),
    path('orders/', views.orderPage, name='orders'),
    path('products/', views.adminProductPage, name='admin_product'),
    path('products/add/', views.adminProductAddPage, name='admin_product_add'),
]
# urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
