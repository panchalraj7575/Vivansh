from django.contrib import admin
from .models import User, Booking
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    # Fields to display in the admin detail view
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Fields to display in the admin create user form
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    search_fields = ("email",)  # Search by email
    ordering = ("email",)  # Order by email
    filter_horizontal = ("groups", "user_permissions")  # Manage groups and permissions


class BookingAdmin(admin.ModelAdmin):
    model = Booking
    list_display = ("user__email", "booking_date", "booking_type")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Booking, BookingAdmin)
