from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


@register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ("email", "auth_provider", "is_active")
    list_filter = (
        "email",
        "auth_provider",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password", "auth_provider")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_verify")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
