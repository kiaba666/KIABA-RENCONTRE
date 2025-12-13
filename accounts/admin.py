from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("KIABA", {"fields": ("role", "phone_e164", "is_verified")}),
    )
    list_display = ("username", "email", "role", "is_active", "is_staff", "is_verified")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "is_verified")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "display_name", "city", "country")
    search_fields = ("user__username", "display_name")


# Register your models here.
