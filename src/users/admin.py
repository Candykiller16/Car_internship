from django.contrib import admin
from src.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_dealer",
        "is_customer",
        "is_showroom",
    )
    list_filter = (
        "is_dealer",
        "is_customer",
        "is_showroom",
    )
