from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, Profile, AdditionalImage, Cart
from django.db.models import Q
from django.contrib import messages
from django.db.models.functions import Lower
from django.core.paginator import Paginator
from .utils.delete_file import delete_file
from .utils.upload_file import upload_file

# Create your views here.

def homePage(request):
    plants=Product.objects.order_by('-created_at')[:12]
    return render(request, 'base/home.html', {"plants":plants})


def productPage(request):
    plants=Product.objects.all()
    paginator=Paginator(plants,12)
    page_number=request.GET.get('page')
    plantsFinal=paginator.get_page(page_number)
    totalPageNumber=plantsFinal.paginator.num_pages
    context={
        'plants':plantsFinal,
        'lastpage':totalPageNumber,
        'totalPageList':[n+1 for n in range(totalPageNumber)],
        }
    return render(request, 'base/product.html', context)

@login_required(login_url="/login/")
def productDetailPage(request, pk):
    plant=Product.objects.get(id=pk)
    recent_products = Product.objects.order_by('-created_at').exclude(id=pk)[:4]
    extraImages=AdditionalImage.objects.filter(product=plant)
    context={"plant":plant,"extraImages":extraImages,"recent_products":recent_products}
    return render(request, 'base/product_detail.html',context)

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
            messages.error(request, 'Incorrect username or password or email. Please enter the correct credentials.')
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
        # print(first_name, last_name, email, username, password)
        if User.objects.filter(Q(username=username) & Q(email=email)).exists():
            messages.error(request, "Username or email is already taken, provide differents one")
            return redirect("signup")
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username is already taken, provide different one")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email is already taken, provide different one")
            return redirect('signup')
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
    if request.method=="POST":
        search_query=request.POST.get('query')
        plants=Product.objects.all()
        if search_query:
            plants=plants.annotate(lower_name=Lower('name')).filter(lower_name__icontains=search_query.lower())
    else:
        plants=Product.objects.all()
    paginator=Paginator(plants,10)
    page_number=request.GET.get('page')
    plantsFinal=paginator.get_page(page_number)
    totalPageNumber=plantsFinal.paginator.num_pages
    context={
        'plants':plantsFinal,
        'lastpage':totalPageNumber,
        'totalPageList':[n+1 for n in range(totalPageNumber)],
        }
    return render(request, 'base/profile/product.html', context)

@login_required(login_url="/login/")
def adminProductAddPage(request):
    if(request.user.profile.role != "Seller"):
        return HttpResponse("You are not allowed to access this page")
    if request.method == "POST":
        name=request.POST.get('name')
        description=request.POST.get('description')
        price=request.POST.get('price')
        discount=request.POST.get('discount') if request.POST.get('discount') else 0
        stock=request.POST.get('stock') if request.POST.get('stock') else 0
        featured_image=request.FILES.get('featured_image')
        additional_images=request.FILES.getlist('additional_images')
        if(featured_image):
            featured_image=upload_file('static/assets/images', 'static/assets/images', featured_image)
        product=Product(
            name=name,
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
        return redirect('admin_product')
    return render(request, 'base/profile/product_add.html',{'action':'save'})

@login_required(login_url="/login/")
def editProduct(request,pk):
    plant=Product.objects.get(id=pk)
    additional_images=AdditionalImage.objects.filter(product=plant)
    if request.method == "POST":
        plant.name=request.POST.get('name')
        plant.description=request.POST.get('description')
        plant.price=request.POST.get('price')
        plant.discount=request.POST.get('discount') if request.POST.get('discount') else 0
        plant.stock=request.POST.get('stock') if request.POST.get('stock') else 0
        updated_featured_image=request.FILES.get('featured_image')
        if(updated_featured_image):
            delete_file(str(plant.featured_image))
            new_featured_image=upload_file('static/assets/images', 'static/assets/images', updated_featured_image)
            plant.featured_image=new_featured_image
        updated_additional_images=request.FILES.getlist('additional_images')
        if(updated_additional_images):
            for old_img in additional_images:
                delete_file(str(old_img.image))
                old_img.delete()
            for image in updated_additional_images:
                update_image = upload_file('static/assets/images', 'static/assets/images', image)
                additional_image = AdditionalImage(product=plant, image=update_image)
                additional_image.save()
        plant.save()
        return redirect('admin_product')
    return render(request,'base/profile/product_add.html',{'action':'edit','plants':plant,'additional_image':additional_images})

@login_required(login_url="/login/")
def deleteProduct(request,pk):
    plant=Product.objects.get(id=pk)
    delete_file(str(plant.featured_image))
    additional_image=AdditionalImage.objects.filter(product=plant)
    for add_img in additional_image:
        delete_file(str(add_img.image.path))
    plant.delete()
    return redirect('admin_product')

@login_required(login_url="/login/")
def addToCart(request,pk):
    quantity=1
    if(request.method == "GET") :
        quantity=int(request.GET.get('quantity'))

    plant=Product.objects.get(id=pk)

    if(quantity == 0):
        cart = Cart.objects.get(product__id=pk)
        if(cart):
            plant.stock += cart.quantity
            plant.save()
            cart.delete()
        return redirect('home')

    if(plant.stock < quantity):
        messages.error(request, 'Not enough stock available')
        return redirect('product_detail', pk=pk)
    
    plant.stock -= quantity
    plant.save()

    obj, cart = Cart.objects.update_or_create(user=request.user, product=plant)
    obj.quantity += quantity
    if(obj.quantity == 0):
        obj.delete()
    else:
        obj.save()
    return redirect('home')