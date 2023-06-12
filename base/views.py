from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, Profile, AdditionalImage
from .utils.delete_file import delete_file
from .utils.upload_file import upload_file

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
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
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
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        password=request.POST.get("password")
        print(first_name, last_name, email, username, password)
        my_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        profile = Profile.objects.create(user=my_user)
        profile.save()
        my_user.save()
        return redirect("login")
    return render(request, 'base/auth/signup.html')

@login_required(login_url="/login/")
def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url="/login/")
def profilePage(request):
    print(request.user.profile.role)
    if(request.method == "POST"):
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        avatar=request.FILES.get("avatar")
        user=request.user
        user.first_name=first_name
        user.last_name=last_name
        avatar_url=""
        if(avatar):
            avatar_url=upload_file('static/assets/images', 'static/assets/images', avatar)
            if(user.profile.avatar):
                delete_file(str(user.profile.avatar))
        Profile.objects.filter(user=user).update(address=address, phone=phone, avatar=avatar_url if avatar else user.profile.avatar)
        user.save()
        return redirect("profile")
    return render(request, 'base/profile/profile.html')

@login_required(login_url="/login")
def orderPage(request):
    return render(request, 'base/profile/order.html', {'range': range(1, 5)})


@login_required(login_url="/login/")
def adminProductPage(request):
    if(request.user.profile.role != "Seller"):
        return HttpResponse("You are not allowed to access this page")
    plants=Plant.objects.all()
    context={'plants':plants}
    return render(request, 'base/profile/product.html', context)

@login_required(login_url="/login/")
def adminProductAddPage(request):
    if(request.user.profile.role != "Seller"):
        return HttpResponse("You are not allowed to access this page")
    if(request.user.profile.role != "Seller"):
        return HttpResponse("You are not allowed to access this page")
    if request.method == "POST":
        name=request.POST.get('name')
        description=request.POST.get('description')
        price=request.POST.get('price')
        discount=request.POST.get('discount')
        stock=request.POST.get('stock')
        featured_image=request.FILES.get('featured_image')
        additional_images=request.FILES.getlist('additional_images')
        if(featured_image):
            featured_image=upload_file('static/assets/images', 'static/assets/images', featured_image)
        product=Product(
            name=name,
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        stock = request.POST.get('stock')
        featured_image = request.FILES.get('featured_image')
        additional_images = request.FILES.getlist('additional_images')

        if featured_image is not None:
            featured_image_url=upload_file('static/assets/images', 'static/assets/images', featured_image)
        else:
            print("Failed")

        plant = Plant(
            plant_name=name,
            description=description,
            price=price,
            discount=discount,
            stock=stock,
            featured_image=featured_image,
            created_by=request.user
        )
        product.save()
        if(additional_images):
            for image in additional_images:
                add_image=upload_file('static/assets/images', 'static/assets/images', image)
                additional_image = AdditionalImage(product=product, image=add_image)
                additional_image.save()
    return render(request, 'base/profile/product_add.html')