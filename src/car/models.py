from django.db import models
from django.db.models.functions import datetime

from core.abstract_models import Statuses


class Car(Statuses):
    BODY_TYPES = [
        ('Hatchback', 'HATCHBACK'),
        ('Minivan', 'MINIVAN'),
        ('CrossOverVehicle', 'CROSSOVERVEHICLE'),
        ('Coupe', 'COUPE'),
        ('Supercar', 'SUPERCAR'),
        ('Cabriolet', 'CABRIOLET'),
        ('Sedan', 'SEDAN'),
        ('Micro', 'MICRO'),

    ]
    TRANSMISSION = [
        ('Automation', 'AUTOMATION'),
        ('Mechanics', 'MECHANICS'),
    ]

    name = models.CharField(max_length=250, null=True, blank=True)
    model = models.CharField(max_length=250, null=True, blank=True, help_text="Car's model")
    body_type = models.CharField(max_length=20,
                                 choices=BODY_TYPES,
                                 default='Hatchback')
    transmission_type = models.CharField(max_length=20,
                                         choices=TRANSMISSION,
                                         default='Automation')
    color = models.CharField(max_length=50, help_text="<b>Car's color</b>", null=True, blank=True)
    year = models.PositiveIntegerField(default=datetime.datetime.today().year, help_text="<b>Year of production</b>",
                                       null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, help_text="<b>The initial price of the car</b>",
                                null=True, blank=True)
    showroom = models.ForeignKey(
        "showroom.Showroom",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="showrooms_cars",
    )
    dealer = models.ForeignKey(
        "dealer.Dealer",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="dealers_cars",
    )
    customer = models.ForeignKey(
        "customer.Customer",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="customers_cars",
    )

    class Meta:
        db_table = "car"

    def __str__(self):
        return f"{self.name} Model {self.model} {self.color}"
