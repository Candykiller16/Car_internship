from core.abstract_models import Info, Statuses, Discount
from django.db import models
from src.users.models import CustomUser
from core.data_and_funcs import default_showroom_priorities


class Showroom(Statuses, Info):
    """ Showroom """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="showroom", null=True, blank=True)
    priorities = models.JSONField(
        encoder=None,
        decoder=None,
        default=default_showroom_priorities,
    )

    class Meta:
        db_table = "showroom"

    def __str__(self):
        return f"{self.name} - {self.email} - {self.country}"


class DiscountShowroom(Statuses, Discount):
    showrooms_discount = models.ForeignKey(
        Showroom,
        on_delete=models.PROTECT,
        related_name="showroom_with_discount",
        null=True,
        verbose_name="showroom",

    )
    discount_showroom_for_car = models.ForeignKey(
        "car.Car",
        on_delete=models.PROTECT,
        related_name="showroom_car_on_sale",
        null=True,
        verbose_name="car",
    )

    class Meta:
        db_table = "showroom_discount"

    def __str__(self):
        return f"{self.showrooms_discount.name} discount equal to {self.amount_of_discount} % started" \
               f" {self.start_date.strftime('%m/%d/%Y')} and will end {self.end_date.strftime('%m/%d/%Y')}"
