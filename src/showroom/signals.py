import random
from django.db.models.signals import post_save, post_delete
from src.showroom.models import Showroom
from src.users.models import CustomUser
from core.data_and_funcs import cars_models, get_random_color, get_random_body_type, get_random_transmission, \
    get_random_year

default_name = random.choice(list(cars_models.keys()))
default_model = random.choice(list(cars_models[default_name]))


def createShowroom(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.is_showroom:
            showroom = Showroom.objects.create(
                user=user,
                email=user.email,
                name=user.first_name,
                country='BY',
                balance=random.randint(10000, 100000),
                priorities={"name": default_name,
                            "model": default_model,
                            "color": get_random_color(),
                            "year": get_random_year(),
                            "body_type": get_random_body_type(),
                            "transmission": get_random_transmission()}
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
