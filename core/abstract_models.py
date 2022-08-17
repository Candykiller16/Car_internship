from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField


class Info(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=20, decimal_places=2, default=0.00
    )
    country = CountryField(null=True, blank=True)
    email = models.EmailField(max_length=250)

    class Meta:
        abstract = True


class Statuses(models.Model):
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def thirty_day_hence():
    return timezone.now() + timezone.timedelta(days=30)


class Discount(models.Model):
    bio = models.TextField(null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=thirty_day_hence)

    class Meta:
        abstract = True


class Created(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
