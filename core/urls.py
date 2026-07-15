from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm

urlpatterns = [
    path("register/", views.register, name="register"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("login/", LoginView.as_view(template_name="core/login.html", authentication_form=LoginForm,),name="login"),
    path("logout/", LogoutView.as_view(next_page="login"),name="logout"),
    path("", views.home, name="home"),
    path("catalog/",views.catalog,name="catalog"),
    path("catalog/<int:pk>",views.product_detail, name ="product_detail"),
    path("dashboard/products",views.dashboard_products,name='dashboard_products'),
    path("dashboard/products/<pk>/edit",views.edit_product, name='edit_product'),
    path("dashboard/products/<pk>/delete",views.delete_product, name='delete_product'),
    path("dashboard/products/<pk>/toggle",views.toggle_status, name='toggle_status'),
    path("dashboard/products/create",views.create_product, name='create_product'),
    path("dashboard/profile/",views.profile,name="profile"),
]
