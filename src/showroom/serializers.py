from django.db.models import Count, F
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from src.showroom.models import Showroom
from src.car.models import Car
from src.car.serializers import CarSerializer
from src.customer.serializers import CustomerShortInfoSerializer


class ShowroomSerializer(CountryFieldMixin, serializers.ModelSerializer):
    cars = serializers.SerializerMethodField()
    total_cars = serializers.SerializerMethodField()
    buyers = serializers.SerializerMethodField()

    class Meta:
        model = Showroom
        fields = ["name", "country", "email", "balance", "is_active", "total_cars", "cars", "buyers"]

    def get_total_cars(self, instance):
        return instance.showrooms_cars.all().count()

    def get_cars(self, instance):
        queryset = Car.objects.filter(showroom=instance.id)
        serializer_data = CarSerializer(queryset, many=True, read_only=True).data
        return serializer_data

    def get_buyers(self, instance):
        queryset = Showroom.objects.get(pk=instance.id)
        buyers = (
            queryset.showroom_that_sells.all()
            .values(name=F("customer__name"))
            .distinct()
            .order_by("customer__name")
        )
        serializer_data = CustomerShortInfoSerializer(buyers, many=True).data

        return serializer_data


class ShowroomShortInfoSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Showroom
        fields = ["name"]
