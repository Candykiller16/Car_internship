from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from src.users.models import CustomUser
from core.abstract_models import Info, Statuses
from core.data_and_funcs import default_showroom_priorities


class Customer(Statuses, Info):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(
        validators=[MinValueValidator(14), MaxValueValidator(150)], null=True, blank=True
    )
    sex = models.CharField(max_length=6, null=True, blank=True)

    class Meta:
        db_table = "customer"

    def __str__(self):
        return f"{self.name} {self.age} years"


class CustomerOffer(Statuses):
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="customer_offers", null=True, blank=True,
    )
    selected_car = models.JSONField(encoder=None,
                                    decoder=None,
                                    default=default_showroom_priorities)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    class Meta:
        db_table = "customer_offer"

    def __str__(self):
        return f"Customer {self.customer} is looking for a {self.price} $ car"
