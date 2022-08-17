from django.contrib import admin

from src.showroom.models import Showroom, DiscountShowroom, ShowroomLoyalty


@admin.register(Showroom)
class ShowroomAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
        "total_cars",
        "unique_buyers",
    )
    list_filter = (
        "name",
        "country",

    )

    # list_display = ('unique_buyers',)
    # list_display_links = ('unique_buyers',)

    def total_cars(self, instance):
        return Showroom.objects.get(pk=instance.id).showrooms_cars.values("name").count()

    def unique_buyers(self, instance):
        buyers = list(Showroom.objects.get(pk=instance.pk).showroom_that_sells.values("customer__name").distinct())
        list_of_buyers = [i["customer__name"] for i in buyers]

        return ',\n\n'.join(list_of_buyers)

    #
    # buyers = list(Showroom.objects.get(pk=instance.pk).showroom_that_sells.values("customer__id").distinct())
    # buyers_id = [i["customer__id"] for i in buyers]
    # lists = []
    # for i in buyers_id:
    #     lists.append(format_html("<a href='/admin/customer/customer/{number}/change/</a>",
    #                              number=i))
    #
    # return ',\n\n'.join(lists)

    # unique_buyers.allow_tags = True


@admin.register(DiscountShowroom)
class DiscountShowroomAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )
    list_filter = (
        "start_date",
        "end_date",
        "is_active",
        "is_active",
        "car",
        "showroom",
    )


@admin.register(ShowroomLoyalty)
class LoyaltyShowroomAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )
    list_filter = (
        "discount",
        "bought_cars",
        "loyalty_count",
        "showroom",
        "customer",
    )
