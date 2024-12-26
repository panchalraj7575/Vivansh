from django import forms
from .models import User, Booking
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True, label="First Name")
    last_name = forms.CharField(max_length=100, required=True, label="Last Name")

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = (
            "booking_date",
            "booking_type",
            "booking_slot",
            "booking_from",
            "booking_to",
        )

    def clean(self):
        cleaned_data = super().clean()

        booking_type = cleaned_data.get("booking_type")
        booking_slot = cleaned_data.get("booking_slot")
        booking_from = cleaned_data.get("booking_from")
        booking_to = cleaned_data.get("booking_to")

        if booking_type == "HALF-DAY" and not booking_slot:
            raise forms.ValidationError("Please select a booking slot.")

        if booking_type == "CUSTOM":
            if not booking_from or not booking_to:
                raise forms.ValidationError(
                    "booking_from and booking_to both are must in Custom booking type."
                )

            if booking_from >= booking_to:
                raise forms.ValidationError(
                    "Booking from can't be greater or equal to booking_to."
                )

        return cleaned_data
