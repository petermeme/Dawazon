from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Vendor
from commodities.models import Product

from login.forms import ProductForm, vendor_SignUp, vendor_Login

def become_vendor(request):
    form = vendor_SignUp()
    if request.method == 'POST':
        form = vendor_SignUp(request.POST)
        if form.is_valid():
            user = form.save()
            username1 = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            login(request, user)
            vendor = Vendor.objects.create(name=user.username1, created_by=user)
            #user = authenticate(username=username, password=password)
            
            messages.success(request, ("Account created"))
            return redirect('vendor_admin')
        else:
            messages.success(request, ("ERROR!! Check requirements"))
            return redirect("become_vendor")
    else:
        return render(request, 'become_vendor.html', {'form': form})

'''    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('home')
    else:
        form = UserCreationForm() 

    return render(request, 'become_vendor.html', {'form': form})
'''

'''def vendor_login(request):
    if request.method == 'POST':
        if form.is_valid():
            username = request.POST['username']
            vendor_password = request.POST['password']
            vendor = authenticate(request, username=username, password=password)
            if vendor is not None:
                login(request, vendor)
                return redirect('vendor_admin')
                messages.success(request, ("You have been logged In!!"))

            else:
                return redirect('vendor-login')
                messages.success(request, ("ERROR!!"))
    else:
        return render(request, 'vendor_login.html', {})
'''
@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    vendor = request.user.vendor
    product = vendor.products.get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.save()

            return redirect('vendor_admin')
    
    return render(request, 'edit_vendor.html', {'vendor': vendor})

def vendors(request):
    vendors = Vendor.objects.all()

    return render(request, 'vendors.html', {'vendors': vendors})

def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    return render(request, 'vendor.html', {'vendor': vendor})

