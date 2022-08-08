from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import datetime

from core.abstract_models import Info, Statuses, Discount

from src.dealer.utils import DiscountRanks
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


class DiscountDealer(models.Model):
    """
    Discounts Dealer - ShowRoom
    """

    discount = models.IntegerField(
        choices=DiscountRanks.DISCOUNT_CHOICES, default=DiscountRanks.REGULAR
    )
    # bought_cars = models.PositiveIntegerField(default=0, help_text="")
    showroom = models.ForeignKey(
        "showroom.Showroom",
        related_name="showroom_discounts",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    dealer = models.ForeignKey(
        "dealer.Dealer",
        related_name="dealer_discounts",
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    class Meta:
        db_table = "dealer_discount"
        unique_together = ["showroom", "dealer"]

    def __str__(self):
        return f"Discount {self.discount} % from '{self.dealer}' to '{self.showroom.name}'"
