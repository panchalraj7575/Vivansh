from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserRegister.as_view(), name="register"),
    path("", views.HomeView.as_view(), name="home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
]
