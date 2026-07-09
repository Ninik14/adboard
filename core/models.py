from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    phone = models.CharField(max_length=20,blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
CATEGORY_CHOICES = [
    ("phones", "ტელეფონები"),
    ("laptops", "ლეპტოპები"),
    ("appliances", "საყოფაცხოვრებო ტექნიკა"),
    ("tablets", "ტაბლეტები"),
    ("tvs", "ტელევიზორები"),
]

STATUS_CHOICES = [
    ("available", "Available"),
    ("sold", "Sold"),
]

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="products/",blank=True,null=True)
    seller = models.ForeignKey(User,on_delete=models.CASCADE,related_name="products")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="available")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
