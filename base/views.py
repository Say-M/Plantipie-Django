from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'base/home.html', {'range': range(1, 13)})

def product(request):
    return render(request, 'base/product.html', {'range': range(1, 13)})

def product_detail(request, id):
    return render(request, 'base/product_detail.html', {'range': range(1, 5)})

def checkout(request):
    return render(request, 'base/checkout.html')

def login(request):
    return render(request, 'base/auth/login.html')

def signup(request):
    return render(request, 'base/auth/signup.html')