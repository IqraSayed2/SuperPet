from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login,logout
from product.models import Product

def home(request):
    return render(request,"index.html")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def register(request):
    if request.method=="GET":
        # form = UserCreationForm()
        form = CustomUserCreationForm()
        return render(request,"register.html",{"form":form})
    elif request.method=="POST":
        message=None
        #form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            message="User Registered Successfully"
        return render(request,"register.html",{"form":form, "message":message})

def user_login(request):
    if request.method == "GET":
        return render(request,"login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        message = None
        if user is not None:
            login(request,user)
            return HttpResponseRedirect("/products")
        message = "Login Failed"
        return render(request,"login.html",{"message":message})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login")

def search(request):
    keyword = request.GET.get('search')
    products = Product.objects.filter(product_name__icontains=keyword)
    context = { "products": products }
    return render(request,"search.html",context)

def template_filters_example(request):
    return render(request,"demo.html",{"data":"Django"})

def profile(request):
    return render(request,'profile.html')