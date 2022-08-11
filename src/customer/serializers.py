from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from src.customer.models import Customer, CustomerOffer


class CustomerShortInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "name",
        ]


class CustomerOfferListSerializer(serializers.ModelSerializer):
    customer = CustomerShortInformationSerializer()

    class Meta:
        model = CustomerOffer
        fields = [
            "id",
            "customer",
            "price",
            "selected_car",
            'is_active',
        ]


class CustomerOfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOffer
        fields = [
            "price",
            "selected_car",
            'is_active',
        ]


class CustomerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    customer_offers = CustomerOfferCreateSerializer(read_only=True, many=True)

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "email",
            "balance",
            "country",
            "age",
            "sex",
            "customer_offers",
        ]


class CustomerShortInfoSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name"]
