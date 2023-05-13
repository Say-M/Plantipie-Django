from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Plant
from .forms import PlantForm

# Create your views here.

def home(request):
    return render(request, 'base/home.html', {'range': range(1, 13),'curUser':""})

@login_required(login_url="/login")
def product(request):
    # plants=Plant.objects.all()
    # context={'plants':plants}
    context=""
    return render(request, 'base/product.html', context)

@login_required(login_url="/login")
def product_detail(request, pk):
    context=""
    # plant=get_object_or_404(Plant,id=pk)
    # context={"plant":plant}
    return render(request, 'base/product_detail.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        user=authenticate(request,username=email,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request, 'base/auth/login.html')

@login_required(login_url="/login")
def create_plant_item(request):
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant=form.save(commit=False)
            plant.save()
            return redirect('home')
    else:
        form = PlantForm()
    return render(request,'base/create_plant_item.html',{'form': form})

@login_required(login_url="/login")
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
        return redirect("login")
    return render(request, 'base/auth/signup.html')