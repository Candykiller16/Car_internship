from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsCustomerUser
from src.customer.models import Customer, CustomerOffer
from src.customer.serializers import CustomerOfferCreateSerializer, CustomerSerializer, CustomerOfferListSerializer


class CustomerViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [(IsAdminUser | IsCustomerUser)]
    search_fields = ("name",)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            customer = Customer.objects.all()
            serializer = self.get_serializer(customer, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.request.user.is_superuser:
            serializer = self.get_serializer(Customer.objects.get(id=pk))
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request, *args, **kwargs):
        if request.user.is_customer:
            customer = self.request.user.customer
            if request.method == 'GET':
                serializer = self.get_serializer(customer)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            elif request.method == 'PUT':
                serializer = self.get_serializer(customer, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk=None):
        if request.user.is_superuser:
            customer = self.get_object()
            serializer = self.get_serializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"customer": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class CustomerOfferViewSet(GenericViewSet):
    """
    To let Customer or Admin create, update, delete information about Customer's offer
    """

    queryset = CustomerOffer.objects.all()
    serializer_class = CustomerOfferCreateSerializer
    permission_classes = [(IsAdminUser | IsCustomerUser)]

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            offers = CustomerOffer.objects.all()
            serializer = CustomerOfferListSerializer(offers, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.is_customer:
            offers = CustomerOffer.objects.filter(customer=request.user.customer)
            serializer = CustomerOfferListSerializer(offers, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.request.user.is_superuser:
            offer = CustomerOffer.objects.get(id=pk)
            serializer = CustomerOfferListSerializer(offer, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.is_customer:
            offer = CustomerOffer.objects.get(id=pk)
            if offer.customer == request.user.customer:
                serializer = CustomerOfferListSerializer(offer, many=False)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': "You see this because you are not the owner of this offer"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk=None):
        offer = CustomerOffer.objects.get(id=pk)
        if request.user.is_superuser:
            serializer = CustomerOfferCreateSerializer(offer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"customer_offer": serializer.data}, status=status.HTTP_200_OK)
        elif self.request.user.is_customer:
            offer = CustomerOffer.objects.get(id=pk)
            if offer.customer == request.user.customer:
                serializer = CustomerOfferListSerializer(offer, many=False)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': "You can't update this offer because you are not the owner of this offer"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        if request.user.is_customer:
            data = self.request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid()
            offer = CustomerOffer.objects.create(
                customer=self.request.user.customer,
                price=serializer.validated_data['price'],
                selected_car=serializer.validated_data['selected_car']
            )
            return Response(data=CustomerOfferCreateSerializer(offer).data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['GET', 'PUT'], url_path='deactivate')
    def deactivate_customer_offer(self, request, pk=None):
        customer_offer = CustomerOffer.objects.get(id=pk)
        if request.user.is_superuser:
            if customer_offer.is_active:
                customer_offer.is_active = False
                customer_offer.save()
            else:
                return Response({'message': 'Offer is already deactivated'}, status=status.HTTP_200_OK)
        elif request.user.is_customer and customer_offer.customer == request.user.customer:
            if customer_offer.is_active:
                customer_offer.is_active = False
                customer_offer.save()
            else:
                return Response({'message': 'Offer is already deactivated'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "You can't update this offer because you are not the owner of this offer"},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({"post": "deactivate offer "}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET', 'PUT'], url_path='activate')
    def activate_customer_offer(self, request, pk=None):
        customer_offer = CustomerOffer.objects.get(id=pk)
        if request.user.is_superuser:
            if not customer_offer.is_active:
                customer_offer.is_active = True
                customer_offer.save()
            else:
                return Response({'message': 'Offer is already active'}, status=status.HTTP_200_OK)
        elif request.user.is_customer and customer_offer.customer == request.user.customer:
            if not customer_offer.is_active:
                customer_offer.is_active = True
                customer_offer.save()
            else:
                return Response({'message': 'Offer is already active'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "You can't update this offer because you are not the owner of this offer"},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({"post": "activate offer "}, status=status.HTTP_200_OK)

#
#
# class CustomerOffersListApiView(views.APIView):
#
#     def get(self, request, pk):
#         customer_offer = CustomerOffer.objects.filter(customer=pk)
#         return Response({"Customer offers": CustomerOfferSerializer(customer_offer, many=True).data},
#                         status=status.HTTP_200_OK)
