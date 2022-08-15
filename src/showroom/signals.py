import random

from django.db.models.signals import post_save, post_delete

from core.data_and_funcs import get_random_name_and_model
from src.showroom.models import Showroom
from src.users.models import CustomUser


def createShowroom(sender, instance, created, **kwargs):
    dictionary = get_random_name_and_model()
    if created:
        user = instance
        if user.is_showroom:
            showroom = Showroom.objects.create(
                user=user,
                email=user.email,
                name=user.first_name,
                country='BY',
                balance=random.randint(10000, 100000),
                price_increase=random.randint(10, 25),
                priorities={"name": list(dictionary.keys())[0],
                            "model": list(dictionary.values())[0],
                            }
            )


def updateShowroom(sender, instance, created, **kwargs):
    showroom = instance
    user = showroom.user

    if created == False:
        user.first_name = showroom.name
        user.email = showroom.email
        user.save()


def deleteShowroom(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createShowroom, sender=CustomUser)
post_save.connect(updateShowroom, sender=Showroom)
post_delete.connect(deleteShowroom, sender=Showroom)
