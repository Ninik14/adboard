from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .models import UserProfile,Product,CATEGORY_CHOICES
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            UserProfile.objects.create(user=new_user)
            login(request,new_user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    
    return render(request,"core/register.html",{'form': form})



@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")


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
    min_price = request.GET.get("min-price","")
    max_price = request.GET.get("max-price","")
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