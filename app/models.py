from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager
from django.core.exceptions import ValidationError
from datetime import time

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Booking(BaseModel):
    BOOKING_TYPES = (
        ("FULL-DAY", "Full-Day"),
        ("HALF-DAY", "Half-Day"),
        ("CUSTOM", "Custom"),
    )
    BOOKING_SLOT_TYPES = (
        ("FIRST-HALF", "First-Half"),
        ("SECOND-HALF", "Second-Half"),
        ("CUSTOM", "Custom"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateField()
    booking_type = models.CharField(max_length=100, choices=BOOKING_TYPES)
    booking_slot = models.CharField(
        max_length=100, choices=BOOKING_SLOT_TYPES, blank=True, null=True
    )
    booking_from = models.TimeField(blank=True, null=True)
    booking_to = models.TimeField(blank=True, null=True)

    def clean(self):
        check_for_bookings = Booking.objects.filter(booking_date=self.booking_date)
        check_full_day_booking = check_for_bookings.filter(
            booking_type="FULL-DAY"
        ).exists()

        if self.booking_type == "FULL-DAY":
            if check_for_bookings.exists():
                raise ValidationError("Booking is not available for selected date.")

        elif self.booking_type == "HALF-DAY":

            if check_full_day_booking:
                raise ValidationError(
                    "Someone has booked for half-day, so full day booking is not available."
                )

            if (
                self.booking_slot == "FIRST-HALF"
                and check_for_bookings.filter(booking_from__lt=time(12, 0)).exists()
            ):
                raise ValidationError("Someone has already booked.")

            if (
                self.booking_slot == "SECOND-HALF"
                and check_for_bookings.filter(booking_from__gte=time(12, 0)).exists()
            ):
                raise ValidationError("Someone has already booked.")

        elif self.booking_type == "CUSTOM":
            if check_full_day_booking:
                raise ValidationError(
                    "Someone has booked for half-day, so full day booking is not available."
                )

            if self.booking_from >= time(0, 0) and self.booking_to <= time(12, 0):
                if check_for_bookings.filter(
                    booking_from__lt=self.booking_to, booking_to__gt=self.booking_from
                ).exists():
                    raise ValidationError(
                        "Someone has already booked during this time in the morning."
                    )

            elif self.booking_from >= time(12, 0) and self.booking_from <= time(23, 59):
                if self.booking_to > time(0, 0) and self.booking_to <= time(12, 0):
                    self.booking_to = time(
                        23, 59
                    )  # Adjust to the last minute of the day
                if check_for_bookings.filter(
                    booking_from__lt=self.booking_to, booking_to__gt=self.booking_from
                ).exists():
                    raise ValidationError(
                        "Someone has already booked during this time in the evening."
                    )
            # if (
            #     self.booking_from >= time(0, 0)
            #     and self.booking_to <= time(12, 0)  # morning
            #     and check_for_bookings.filter(
            #         booking_from__gte=time(0, 0), booking_to__lte=time(12, 0)
            #     ).exists()
            # ):
            #     raise ValidationError("Someone has already booked.")

            # if (
            #     self.booking_from >= time(12, 0)
            #     and self.booking_to <= time(0, 0)
            #     and check_for_bookings.filter(
            #         booking_from__gte=time(12, 0), booking_to__lte=time(0, 0)
            #     ).exists()
            # ):
            #     raise ValidationError("Someone has already booked.")
        return super().clean()
