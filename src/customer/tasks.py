from celery import shared_task
from django.db import transaction
from django.db.models import Q, F

from src.car.models import Car
from src.customer.models import CustomerOffer
from src.showroom.models import DiscountShowroom, ShowroomLoyalty
from src.transaction.models import FromShowroomToCustomerTransaction


@shared_task
def customer_task():
    for offer in CustomerOffer.objects.all():
        if offer.is_active:
            selected_car = offer.selected_car
            selected_car_search = (
                    Q(name__icontains=selected_car.get("name"))
                    & Q(model__exact=selected_car.get("model"))
                    & Q(body_type__exact=selected_car.get("body_type"))
                    & Q(transmission_type__exact=selected_car.get("transmission_type"))
                    & Q(color__icontains=selected_car.get("color"))
                    & Q(year__lte=selected_car.get("year"))
                    & Q(price__lte=selected_car.get("price"))
            )
            showroom_car = Car.objects.filter(
                selected_car_search, dealer__isnull=True, customer__isnull=True
            ).order_by("-price").first()
            # До этого момента всё ОК, машина находится
            if showroom_car:
                with transaction.atomic():
                    discount = 0
                    loyalty = 0
                    customer = offer.customer
                    showroom = showroom_car.showroom
                    if DiscountShowroom.objects.filter(car=showroom_car, showroom=showroom_car.showroom):
                        discount = DiscountShowroom.objects.filter(car=showroom_car,
                                                                   showroom=F("showroom_car__showroom")).discount

                    loyalty_showroom, created = ShowroomLoyalty.objects.get_or_create(customer=customer,
                                                                                      showroom=showroom_car.showroom)
                    if loyalty_showroom.bought_cars >= loyalty_showroom.loyalty_count:
                        loyalty = loyalty_showroom.discount

                    if loyalty > discount:
                        discount = loyalty

                    price = float(showroom_car.price) * ((100 - discount) / 100)

                    if float(customer.balance) - price > 0:
                        FromShowroomToCustomerTransaction.objects.create(
                            showroom=showroom,
                            customer=customer,
                            car=showroom_car,
                            price=price,
                            discount=discount,
                        )
                        showroom.balance += showroom_car.price
                        showroom.save(update_fields=["balance"])
                        showroom_car.showroom = None
                        showroom_car.customer = offer.customer
                        showroom_car.save(
                            update_fields=[
                                "showroom",
                                "customer",
                            ]
                        )
                        customer.balance = float(customer.balance) - price
                        customer.save(update_fields=["balance"])
                        loyalty_showroom.bought_cars += 1
                        loyalty_showroom.save(update_fields=["bought_cars"])
                        offer.is_active = False
                        offer.save(update_fields=["is_active"])
