from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def homePage(request):
    return render(request, 'base/home.html', {'range': range(1, 13),'curUser':""})

def productPage(request):
    return render(request, 'base/product.html', {'range': range(1, 13)})

def productDetailPage(request, id):
    return render(request, 'base/product_detail.html', {'range': range(1, 5)})

@login_required(login_url="/login")
def checkoutPage(request):
    return render(request, 'base/checkout.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email)
        print(password)
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request, 'base/auth/login.html')

def signupPage(request):
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

@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url="/login")
def profilePage(request):
    return render(request, 'base/profile/profile.html')

@login_required(login_url="/login")
def orderPage(request):
    return render(request, 'base/profile/order.html', {'range': range(1, 5)})