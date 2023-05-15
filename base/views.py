from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Plant, Profile
from .utils.delete import delete_file

# Create your views here.

def homePage(request):
    return render(request, 'base/home.html', {'range': range(1, 13),'curUser':""})

def productPage(request):
    return render(request, 'base/product.html', {'range': range(1, 13)})

def productDetailPage(request, id):
    return render(request, 'base/product_detail.html', {'range': range(1, 5)})


# def productPage(request):
#     # plants=Plant.objects.all()
#     # context={'plants':plants}
#     context=""
#     return render(request, 'base/product.html', context)

# @login_required(login_url="/login/")
# def productDetailPage(request, pk):
#     context=""
#     # plant=get_object_or_404(Plant,id=pk)
#     # context={"plant":plant}
#     return render(request, 'base/product_detail.html',context)

@login_required(login_url="/login/")
def checkoutPage(request):
    return render(request, 'base/checkout.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            if(request.GET.get("next")):
                return redirect(request.GET.get("next"))
            return redirect('home')
        else:
            print("Failed")
    return render(request, 'base/auth/login.html')

def signupPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email=request.POST.get("email")
        firstname=request.POST.get("first_name")
        lastname=request.POST.get("last_name")
        password=request.POST.get("password")
        my_user = User.objects.create_user(username=email, password=password, first_name=firstname, last_name=lastname)
        my_user.save()
        return redirect("login")
    return render(request, 'base/auth/signup.html')

@login_required(login_url="/login/")
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url="/login/")
def profilePage(request):
    if(request.method == "POST"):
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        avatar=request.FILES.get("avatar")
        user=request.user
        user.first_name=first_name
        user.last_name=last_name
        fss=FileSystemStorage(location='static/assets/images', base_url='assets/images')
        file=fss.save(avatar.name,avatar)
        if(user.profile.avatar and avatar):
            delete_file('static/' + str(user.profile.avatar))
        Profile.objects.filter(user=user).update(address=address, phone=phone, avatar=fss.url(file) if avatar else user.profile.avatar)
        user.save()
        return redirect("profile")
    return render(request, 'base/profile/profile.html')

@login_required(login_url="/login")
def orderPage(request):
    return render(request, 'base/profile/order.html', {'range': range(1, 5)})


@login_required(login_url="/login/")
def adminProductPage(request):
    plants=Plant.objects.all()
    context={'plants':plants}
    return render(request, 'base/profile/product.html', context)

@login_required(login_url="/login/")
def adminProductAddPage(request):
    return render(request, 'base/profile/product_add.html')