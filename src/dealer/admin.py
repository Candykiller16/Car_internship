from django.contrib import admin

from src.dealer.models import Dealer, DiscountDealer


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
        "number_of_buyers",
        "total_cars",
    )
    list_filter = (
        "name",
        "country",
        "number_of_buyers",
        "is_active",
        "created",
        "updated",
    )

    def total_cars(self, instance):
        return Dealer.objects.get(pk=instance.id).dealers_cars.values("name").count()


@admin.register(DiscountDealer)
class DiscountDealerAdmin(admin.ModelAdmin):
    list_filter = (
        "discount",
        # "bought_cars",
        "showroom",
        "dealer",
    )
