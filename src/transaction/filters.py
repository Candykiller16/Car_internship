from django_filters import rest_framework as filters
from django_filters.rest_framework import FilterSet

from src.transaction.models import FromDealerToShowroomTransaction, FromShowroomToCustomerTransaction


class ShowroomToCustomerFilter(FilterSet):
    model = FromShowroomToCustomerTransaction
    fields = {
        "car__name": ["iexact"],
        "car__model": ["iexact"],
        "customer__name": ["iexact"],
        "showroom__name": ["iexact"],
        "price": ["exact", "lt", "gt"],
        "created": ["exact", "lt", "gt"],
    }


class DealerToShowroomFilter(FilterSet):
    model = FromDealerToShowroomTransaction
    fields = {
        "car__name": ["iexact"],
        "car__model": ["iexact"],
        "dealer__name": ["iexact"],
        "showroom__name": ["iexact"],
        "price": ["exact", "lt", "gt"],
        "created": ["exact", "lt", "gt"],
    }
