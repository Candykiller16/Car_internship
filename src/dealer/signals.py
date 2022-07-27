import random

from django.db.models.signals import post_save, post_delete

from src.dealer.models import Dealer
from src.users.models import CustomUser


def createDealer(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.is_dealer:
            dealer = Dealer.objects.create(
                user=user,
                email=user.email,
                name=user.first_name,
                country='BY',
                found_year=random.randint(1879, 1998),
                balance=random.randint(15000, 100000),
                bio="Lorem Ipsum is simply dummy text of the printing and typesetting industry. "
                    "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, "
                    "when an unknown printer took a galley of type and scrambled it to make a type specimen book. "
                    "It has survived not only five centuries, but also the leap into electronic typesetting, "
                    "remaining essentially unchanged. "
            )


def updateDealer(sender, instance, created, **kwargs):
    dealer = instance
    user = dealer.user

    if created == False:
        user.first_name = dealer.name
        user.email = dealer.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createDealer, sender=CustomUser)
post_save.connect(updateDealer, sender=Dealer)
post_delete.connect(deleteUser, sender=Dealer)
