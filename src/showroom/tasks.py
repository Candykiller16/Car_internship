from decimal import Decimal

from celery import shared_task
from django.db import transaction
from django.db.models import Q

from src.car.models import Car
from src.dealer.models import DiscountDealer, DealerLoyalty
from src.showroom.models import Showroom
from src.transaction.models import FromDealerToShowroomTransaction


def showroom_task_func(car_dealer_search, showroom):
    dealer_car = Car.objects.filter(
        car_dealer_search, showroom__isnull=True, customer__isnull=True
    ).order_by("-price").first()
    if dealer_car:
        with transaction.atomic():
            if DiscountDealer.objects.get(car=dealer_car, dealer=dealer_car.dealer):
                discount = DiscountDealer.objects.get(car=dealer_car,
                                                      dealer=dealer_car.dealer).discount

            loyalty_dealer, created = DealerLoyalty.objects.get_or_create(dealer=dealer_car.dealer,
                                                                          showroom=showroom)
            if loyalty_dealer.bought_cars >= loyalty_dealer.loyalty_count:
                loyalty = loyalty_dealer.discount
            else:
                loyalty = 0

            if loyalty > discount:
                total_discount = loyalty
            else:
                total_discount = discount

            price = float(dealer_car.price) * ((100 - float(total_discount)) / 100)

            if float(showroom.balance) - price > 0:
                FromDealerToShowroomTransaction.objects.create(
                    showroom=showroom,
                    dealer=dealer_car.dealer,
                    car=dealer_car,
                    price=price,
                    discount=total_discount,
                )
                dealer_car.showroom = showroom
                dealer_car.dealer = None
                dealer_car.price = dealer_car.price * Decimal(1 + (showroom.price_increase / 100))
                dealer_car.save(update_fields=["showroom", "dealer", "price"])
                showroom.balance = float(showroom.balance) - price
                showroom.save(update_fields=["balance"])
                loyalty_dealer.bought_cars += 1
                loyalty_dealer.save(update_fields=["bought_cars"])


@shared_task
def showroom_task():
    for showroom in Showroom.objects.all():
        showroom_preferences = showroom.priorities
        if type(showroom_preferences) == type({}):
            car_dealer_search = (Q(name__icontains=showroom_preferences.get("name"))
                                 & Q(model__icontains=showroom_preferences.get("model")))
            showroom_task_func(car_dealer_search=car_dealer_search, showroom=showroom)
        elif type(showroom_preferences) == type([]):
            for showroom_preference in showroom_preferences:
                car_dealer_search = (Q(name__icontains=showroom_preference.get("name"))
                                     & Q(model__icontains=showroom_preference.get("model")))
                showroom_task_func(car_dealer_search=car_dealer_search, showroom=showroom)
