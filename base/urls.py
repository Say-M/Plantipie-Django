from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('product/<str:pk>/', views.product_detail, name='product_detail'),
    path('login', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout',views.logout_user,name='logout'),
    path('create-plant-item',views.create_plant_item,name="create-plant-item"),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)