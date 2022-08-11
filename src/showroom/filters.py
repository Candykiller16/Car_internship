from django_filters.rest_framework import FilterSet

from src.showroom.models import Showroom


class ShowroomFilter(FilterSet):
    class Meta:
        model = Showroom
        fields = {
            "name": ["icontains"],
            "country": ["icontains"],
            "balance": ["exact", "lt", "gt"],
        }
