from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('product/<str:id>/', views.product_detail, name='product_detail'),
    path('login', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout',views.logout_user,name='logout')
]