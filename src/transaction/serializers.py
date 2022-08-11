from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from src.car.serializers import CarSerializer
from src.customer.serializers import CustomerShortInfoSerializer
from src.dealer.serializers import DealerShortInfoSerializer
from src.showroom.serializers import ShowroomShortInfoSerializer
from src.transaction.models import FromShowroomToCustomerTransaction, FromDealerToShowroomTransaction


class FromDealerToShowroomTransactionSerializer(serializers.ModelSerializer):
    dealer = DealerShortInfoSerializer(read_only=True)
    showroom = ShowroomShortInfoSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    class Meta:
        model = FromDealerToShowroomTransaction
        fields = ["dealer", "showroom", "car", 'price', "discount"]


class FromShowroomToCustomerTransactionSerializer(CountryFieldMixin, serializers.ModelSerializer):
    showroom = ShowroomShortInfoSerializer(read_only=True)
    customer = CustomerShortInfoSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    class Meta:
        model = FromShowroomToCustomerTransaction
        fields = ["id", "showroom", "customer", "car", 'price', "discount"]
