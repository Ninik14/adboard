from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product,UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title","description","price","category", "image", "status"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "bio", "avatar"]

