from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Product, Profile, AdditionalImage, Cart, Order, OrderProduct
from django.contrib import messages
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
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        shipping_address = request.POST.get("shipping_address")
        billing_address = request.POST.get("billing_address")
        payment_method = request.POST.get("payment_method")
        transaction_id = request.POST.get("transaction_id") if request.POST.get("transaction_id") else None
        
        order = Order(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            shipping_address=shipping_address,
            billing_address=billing_address,
            payment_method=payment_method,
            transaction_id=transaction_id,
            user=request.user,
        )
        order.save()

        carts = request.user.carts()
        print(carts)
        for cart in carts:
            order_product = OrderProduct(
                order=order,
                product=cart.product,
                quantity=cart.quantity,
                price=cart.product.price,
                discount=cart.product.discount,
            )
            order_product.save()
            cart.delete()
        return redirect('home')

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
    orders = []
    if request.user.profile.role == "Seller":
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)

    context = {
        "orders": orders
    }
    
    return render(request, 'base/profile/order.html', context)

@login_required(login_url="/login")
def orderDetailPage(request, pk):
    order = Order.objects.get(id=pk)
    context = {"order": order}

    if request.method == 'POST':
        status = request.POST.get('status')
        print(status)
        order.status = status
        order.save()
        return redirect('order_detail', pk=pk)

    return render(request, 'base/profile/order_detail.html', context)


@login_required(login_url="/login/")
def adminProductPage(request):
    if(request.user.profile.role != "Seller"):
        return HttpResponse("You are not allowed to access this page")
    plants=Product.objects.all()
    context={'plants':plants}
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
        delete_file(str(add_img.image))
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