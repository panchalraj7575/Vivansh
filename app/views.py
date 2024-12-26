from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import CreateUserForm, BookingForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import time
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class UserRegister(View):
    """
    User register View.
    """

    template = "app/register.html"

    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        return render(request, self.template, {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

        return render(request, self.template, {"form": form})


class LoginView(View):
    """
    User Login View.
    """

    template = "app/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("home")

        return render(request, self.template, {"error": "Invalid Credentials."})


class HomeView(LoginRequiredMixin, View):
    """
    Booking page.
    """

    template = "app/home.html"

    def get(self, request, *args, **kwargs):
        form = BookingForm()
        return render(request, self.template, {"form": form})

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            if booking.booking_type == "HALF-DAY":
                if booking.booking_slot == "FIRST-HALF":
                    booking.booking_from = time(0, 0, 0)
                    booking.booking_to = time(12, 0, 0)
            booking.user = request.user
            booking.save()
            messages.success(request, "Booking created successfully.")
            return redirect("home")

        return render(request, self.template, {"form": form})


class Logout(LoginRequiredMixin, View):
    """
    User Logout View.
    """

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
