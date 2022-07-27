from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_dealer = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_showroom = models.BooleanField(default=False)

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.username}"
