import random

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from src.customer.models import Customer
from src.users.models import CustomUser

sex = ['male', 'female']


def createCustomer(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.is_customer:
            customer = Customer.objects.create(
                user=user,
                email=user.email,
                name=user.first_name,
                age=random.randint(18, 100),
                balance=random.randint(3000, 15000),
                sex=random.choice(sex),
                country='BY',
            )


def updateCustomer(sender, instance, created, **kwargs):
    customer = instance
    user = customer.user

    if created == False:
        user.first_name = customer.name
        user.email = customer.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createCustomer, sender=CustomUser)
post_save.connect(updateCustomer, sender=Customer)
post_delete.connect(deleteUser, sender=Customer)
