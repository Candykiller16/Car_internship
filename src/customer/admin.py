from django.contrib import admin

from src.customer.models import Customer, CustomerOffer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )
    list_filter = (
        "name",
        "age",
        "sex",
        "country",
        "created",
        "updated",
    )


@admin.register(CustomerOffer)
class CustomerOrderAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )
    list_filter = (
        "is_active",
        "created",
        "updated",
    )