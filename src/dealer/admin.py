from django.contrib import admin

from src.dealer.models import Dealer, DiscountDealer, DealerLoyalty


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "total_cars",
        "number_of_buyers",
        "cars_sold",
        "income",
    )

    readonly_fields = (
        "created",
        "updated",
        "number_of_buyers",
        "total_cars",
        "unique_buyers",
        "cars_sold",
        "income",
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

    def unique_buyers(self, instance):
        buyers = list(Dealer.objects.get(pk=instance.pk).dealer_that_sells.values("showroom__name").distinct())
        list_of_buyers = [i["showroom__name"] for i in buyers]

        return ',\n\n'.join(list_of_buyers)

    def cars_sold(self, instance):
        return Dealer.objects.get(pk=instance.id).dealer_that_sells.values("car__name").count()

    def income(self, instance):
        count = 0
        for amount in Dealer.objects.get(pk=instance.id).dealer_that_sells.values("price"):
            count += float(amount['price'])
        return count


@admin.register(DiscountDealer)
class DiscountDealerAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )
    list_filter = (
        "start_date",
        "end_date",
        "discount",
        "is_active",
        "car",
        "dealer",
    )


@admin.register(DealerLoyalty)
class DealerLoyaltyAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )
    list_filter = (
        "discount",
        "bought_cars",
        "loyalty_count",
        "showroom",
        "dealer",
    )
