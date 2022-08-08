from django_filters import rest_framework as filters

from src.dealer.models import Dealer


class DealerFilter(filters.FilterSet):
    class Meta:
        model = Dealer
        fields = {"name": ["iexact"],
                  "number_of_buyers": ["exact", "lt", "gt"],
                  }
