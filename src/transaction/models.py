from django.db import models
from core.abstract_models import Created
from django.core.validators import MinValueValidator, MaxValueValidator


class FromDealerToShowroomTransaction(Created):
    dealer = models.ForeignKey("dealer.Dealer", on_delete=models.PROTECT, related_name="dealer_that_sells", null=True,
                               blank=True)
    showroom = models.ForeignKey("showroom.Showroom", on_delete=models.PROTECT, related_name="showroom_that_buys",
                                 null=True, blank=True)
    car = models.ForeignKey("car.Car", on_delete=models.PROTECT, related_name="car_for_sale", null=True, blank=True)
    discount = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)])  # подумать над реализацией FK на DiscountDealer
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        db_table = "transactions_from_dealer_to_showroom"

    def __str__(self):
        return f" From {self.dealer} to {self.showroom.name} sold {self.car} with {self.discount}% discount"


class FromShowroomToCustomerTransaction(Created):
    showroom = models.ForeignKey("showroom.Showroom", on_delete=models.PROTECT, related_name="showroom_that_sells",
                                 null=True, blank=True)
    customer = models.ForeignKey("customer.Customer", on_delete=models.PROTECT,
                                 related_name="customer_transaction_history", null=True, blank=True)
    car = models.ForeignKey("car.Car", on_delete=models.PROTECT, related_name="car_to_customer")
    discount = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)])  # подумать над реализацией FK на DiscountShowroom
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    class Meta:
        db_table = "transactions_from_showroom_to_customer"

    def __str__(self):
        return f" From {self.showroom.name} to {self.customer.name} sold {self.car} with {self.discount}% discount"
