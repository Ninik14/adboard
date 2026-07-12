from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("register/", views.register, name="register"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("login/", LoginView.as_view(template_name="core/login.html"),name="login"),
    path("logout/", LogoutView.as_view(next_page="login"),name="logout"),
    path("", views.home, name="home"),
    path("catalog/",views.catalog,name="catalog"),
    path("catalog/<int:pk>",views.product_detail, name ="product_detail")
]
