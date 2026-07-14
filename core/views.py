from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm,ProductForm,ProfileForm
from .models import UserProfile,Product,CATEGORY_CHOICES,STATUS_CHOICES
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            UserProfile.objects.create(user=new_user)
            login(request,new_user)
            messages.success(request, "Registration completed successfully.")
            return redirect("dashboard")
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    
    return render(request,"core/register.html",{'form': form})



def home(request):
    total_products = Product.objects.count()

    total_sellers = User.objects.filter(products__isnull = False).distinct().count()

    context = {
        'total_products':total_products,
        'total_sellers':total_sellers,
    }
    
    return render(request, 'core/home.html', context)



def catalog(request):
    products = Product.objects.filter(status="available")

    category = request.GET.get("category","")
    min_price = request.GET.get("min_price","")
    max_price = request.GET.get("max_price","")
    search_by_name = request.GET.get("search","")

    if category:
        products = products.filter(category=category)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    if search_by_name:
        products = products.filter(title__icontains=search_by_name)
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'selected_category':category,
        'categories':CATEGORY_CHOICES,
        'min_price':min_price,
        'max_price':max_price,
        'search':search_by_name,
    }

    return render(request,"core/catalog.html",context)


def product_detail(request,pk):
    product = get_object_or_404(Product,pk=pk)
    context = {
        'product':product
    }

    return render(request,'core/product_detail.html',context)



@login_required
def dashboard(request):
    user_products = Product.objects.filter(seller = request.user)
    
    total_products = user_products.count()
    available = user_products.filter(status = 'available').count()
    sold = user_products.filter(status = 'sold').count()

    last_products = user_products.order_by("-created_at")[:5]

    context = {
        'total_products': total_products,
        'available': available,
        'sold':sold,
        'last_products':last_products,
    }


    return render(request, "core/dashboard.html",context)




@login_required
def dashboard_products(request):
    user_products = Product.objects.filter(seller = request.user)

    status = request.GET.get("status","")
    category = request.GET.get("category","")

    if status:
        user_products = user_products.filter(status=status)
    
    if category:
        user_products = user_products.filter(category=category)
    
    paginator=Paginator(user_products,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'statuses':STATUS_CHOICES,
        'selected_status':status,
        'selected_category':category,
        'categories':CATEGORY_CHOICES,
    }

    return render(request,"core/dashboard_products.html",context)


@login_required
def create_product(request):
    if request.method=='POST':
        form = ProductForm(request.POST,request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()

            messages.success(request,"Product added successfully.")

            return redirect("dashboard_products")
        
        messages.error(request, "Please correct the errors below.")
 
    else:
        form = ProductForm()
    
    return render(request,'core/create_product.html',{'form': form})



@login_required
def edit_product(request,pk):
    product = get_object_or_404(Product,pk=pk)
    if request.user != product.seller:
        messages.warning(request,"You do not have permission to access this product.")
        return redirect("dashboard_products")
    
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)

        if form.is_valid():
            form.save()
            messages.success(request,"Product updated successfully.")
            return redirect("product_detail", pk=product.pk)
        
        messages.error(request,"Please correct the errors below.")

    else:
        form = ProductForm(instance=product)

    context = {
        "form": form,
    }

    return render(request, "core/edit_product.html", context)

@login_required
def delete_product(request,pk):
    product = get_object_or_404(Product,pk=pk)

    if request.user != product.seller:
        messages.warning(request,"You do not have permission to access this product.")
        return redirect("dashboard_products")
    
    if request.method == 'POST':
        product.delete()
        messages.success(request,"Product deleted successfully.")
        return redirect("dashboard_products")
    
    return render(request,"core/delete_product.html",{'product':product})

@login_required
def toggle_status(request,pk):
    product = get_object_or_404(Product,pk=pk)

    if request.user != product.seller:
        messages.warning(request,"You do not have permission to access this product.")
        return redirect("dashboard_products")
    
    if request.method == 'POST':
        if product.status == "available":
            product.status = "sold"
        else:
            product.status = "available"

        product.save()

    return redirect("dashboard_products")


@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("dashboard")
        
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)
    
    return render(request,"core/profile.html",{'form':form})
