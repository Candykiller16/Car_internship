from django.core.validators import MinValueValidator, MaxValueValidator

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
    price_increase = models.PositiveIntegerField(default=13, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                 null=True,
                                                 blank=True, help_text="<b>The coefficient of price increase</b>")

    class Meta:
        db_table = "showroom"

    def __str__(self):
        return f"{self.name} - {self.email} - {self.country}"


class DiscountShowroom(Statuses, Discount):
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    showroom = models.ForeignKey(
        Showroom,
        on_delete=models.PROTECT,
        related_name="showroom_discount",
        null=True,
        verbose_name="showroom",

    )
    car = models.ForeignKey(
        "car.Car",
        on_delete=models.PROTECT,
        related_name="showroom_car_with_discount",
        null=True,
        verbose_name="car",
    )

    class Meta:
        db_table = "showroom_discount"
        unique_together = ["car", "showroom"]

    def __str__(self):
        return f"{self.showroom.name} discount equal to {self.discount} % started" \
               f" {self.start_date.strftime('%m/%d/%Y')} and will end {self.end_date.strftime('%m/%d/%Y')}"


class ShowroomLoyalty(Statuses):
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=10)
    bought_cars = models.PositiveIntegerField(default=0)
    loyalty_count = models.PositiveIntegerField(default=10)
    showroom = models.ForeignKey(
        Showroom,
        related_name="showroom_customer_loyalties",
        on_delete=models.CASCADE,
        null=True,
    )
    customer = models.ForeignKey(
        "customer.Customer",
        related_name="customer_loyalties",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        db_table = "showroom_loyalty"
        unique_together = ["customer", "showroom"]

    def __str__(self):
        return f" Loyalty program from {self.showroom.name} for customer {self.customer.name} with discount equal" \
               f" {self.discount} % if he (she) bought {self.bought_cars} "
