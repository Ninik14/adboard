from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required


def register(request):
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