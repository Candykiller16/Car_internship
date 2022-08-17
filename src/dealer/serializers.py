from django.db.models import F
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers
from src.showroom.serializers import ShowroomShortInfoSerializer
from src.dealer.models import Dealer, DiscountDealer
from src.car.serializers import CarSerializer


class DealerSerializer(CountryFieldMixin, serializers.ModelSerializer):
    dealers_cars = CarSerializer(many=True, read_only=True)
    total_cars = serializers.SerializerMethodField()
    buyers = serializers.SerializerMethodField()

    class Meta:
        model = Dealer
        fields = [
            "id",
            "name",
            "email",
            "found_year",
            "bio",
            "total_cars",
            'is_active',
            'number_of_buyers',
            "dealers_cars",
            "buyers",
        ]

    def get_total_cars(self, instance):
        return instance.dealers_cars.count()

    def get_buyers(self, instance):
        queryset = Dealer.objects.get(pk=instance.pk)
        buyers = (
            queryset.dealer_that_sells.all()
            .values(name=F("showroom__name"))
            .distinct()
            .order_by("showroom__name")
        )
        serializer_data = ShowroomShortInfoSerializer(buyers, many=True).data
        return serializer_data


class DealerShortInfoSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ["name"]


class DiscountDealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountDealer
        fields = "__all__"
