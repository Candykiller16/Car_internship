from rest_framework import serializers

from src.car.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["name", "model", "body_type", "transmission_type", "color", "year", "price"]


class ShortInfoCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["name", "model"]
