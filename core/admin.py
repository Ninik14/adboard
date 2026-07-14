from django.contrib import admin
from .models import UserProfile,Product

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "phone",
    ]

    search_fields = [
        "user__username",
        "phone",
    ]
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "seller",
        "price",
        "category",
        "status",
    ]

    list_filter = [
        "category",
        "status",
    ]

    search_fields = [
        "title",
        "description",
    ]

    list_editable = [
        "status",
    ]


