from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsDealerUser, IsCustomerUser
from src.dealer.filters import DealerFilter
from src.dealer.models import Dealer
from src.dealer.serializers import DealerSerializer


class DealerViewSet(mixins.RetrieveModelMixin,
                    GenericViewSet):
    """
    Viewset to see information about Dealers
    """
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [(IsAdminUser | IsDealerUser | IsCustomerUser)]
    filterset_class = DealerFilter
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name",)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_customer:
            dealer = Dealer.objects.all()
            serializer = self.get_serializer(dealer, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_customer:
            serializer = self.get_serializer(Dealer.objects.get(id=pk))
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request, *args, **kwargs):
        if request.user.is_dealer:
            dealer = self.request.user.dealer
            if request.method == 'GET':
                serializer = self.get_serializer(dealer)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            elif request.method == 'PUT':
                serializer = self.get_serializer(dealer, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk=None):
        if request.user.is_superuser:
            dealer = self.get_object()
            serializer = self.get_serializer(dealer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"dealer": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
