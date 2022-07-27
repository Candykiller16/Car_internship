from django.contrib import admin

from src.car.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )
    list_filter = (
        "name",
        "model",
        "body_type",
        "transmission_type",
        "color",
        "year",
        'dealer',
        "showroom",
        "customer",
    )