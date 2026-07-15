from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product,UserProfile
from django.contrib.auth.forms import AuthenticationForm



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title","description","price","category", "image", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        for field in ["category", "status"]:
            self.fields[field].widget.attrs["class"] = "form-select"

        self.fields["description"].widget.attrs["rows"] = 5


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "bio", "avatar"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["bio"].widget.attrs["rows"] = 5



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username" }))

    password = forms.CharField(widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",}))
