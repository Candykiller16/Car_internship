from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import datetime

from core.abstract_models import Info, Statuses, Discount
from src.users.models import CustomUser


class Dealer(Statuses, Info):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="dealer", null=True, blank=True)
    found_year = models.PositiveIntegerField(default=datetime.datetime.today().year, null=True, blank=True)
    bio = models.TextField(null=True)
    number_of_buyers = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "dealer"

    def __str__(self):
        return f"{self.name}"


class DiscountDealer(Discount, Statuses):
    """
    Discounts Dealer - ShowRoom
    """
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    car = models.ForeignKey(
        "car.Car",
        related_name="discount_dealer_car",
        on_delete=models.CASCADE,
        null=True,
    )
    dealer = models.ForeignKey(
        "dealer.Dealer",
        related_name="dealer_discounts",
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    class Meta:
        db_table = "dealer_discount"
        unique_together = ["car", "dealer"]

    def __str__(self):
        return f"Discount {self.discount} % from '{self.dealer}' for '{self.car}'"


class DealerLoyalty(Statuses):
    discount = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=10)
    bought_cars = models.PositiveIntegerField(default=0)
    loyalty_count = models.PositiveIntegerField(default=10)
    showroom = models.ForeignKey(
        "showroom.Showroom",
        related_name="dealer_showroom_loyalties",
        on_delete=models.CASCADE,
        null=True,
    )
    dealer = models.ForeignKey(
        "dealer.Dealer",
        related_name="dealer_loyalties",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        db_table = "dealer_loyalty"
        unique_together = ["showroom", "dealer"]

    def __str__(self):
        return f" Loyalty program from {self.dealer} to {self.showroom}"
