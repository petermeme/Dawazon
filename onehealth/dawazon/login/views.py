from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, SignUpForm, UpdateUserForm
from .models import Product
from django import forms 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


# Create your views here.
# Home page
def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products':products})

def root(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# signup page
def user_signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Account created"))
            return redirect('prfile')
        else:
            messages.success(request, ("ERROR!! Check requirements"))
            return redirect("signup")
    else:
        return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged In!!"))
            return redirect('profile')
        else:
            messages.success(request, ("ERROR!!"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

# logout page
def user_logout(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect('home')

def user_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id) # Each user has a unique user id
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "Update successful!!")
            return redirect('home')
        return render(request, "profile.html", {'user_form':user_form})

    else:
        messages.success(request, "Please Login")
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request, foo):
    # Replace hyphens  with spaces
    foo = foo.replace('-', '')
    #grab the category from url
    try:
        # look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})

    except:
        messages.success(request, "Does Not Exist")
        return redirect('home')
