from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'base/home.html', {'range': range(1, 13),'curUser':""})

def product(request):
    return render(request, 'base/product.html', {'range': range(1, 13)})

@login_required(login_url="/login")
def product_detail(request, id):
    return render(request, 'base/product_detail.html', {'range': range(1, 5)})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email)
        print(password)
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request, 'base/auth/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email=request.POST.get("email")
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        password=request.POST.get("password")
        my_user = User.objects.create_user(username=email, password=password, first_name=firstname, last_name=lastname)
        my_user.save()
        print("success")
        return redirect("login")
    return render(request, 'base/auth/signup.html')