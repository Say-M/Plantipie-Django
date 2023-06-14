from django.urls import path
from . import views

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
    path('delete/<int:pk>/', views.deleteProduct , name='delete_view'),
    path('product/edit/<int:pk>',views.editProduct,name="edit_product"),
    path('product/add_to_cart/<int:pk>',views.addToCart,name="addToCart")

]
# urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
