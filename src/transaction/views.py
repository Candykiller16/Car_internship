from django.db.models import Q
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser

from core.permissions import IsDealerUser, IsShowroomUser, IsCustomerUser
from src.transaction.filters import DealerToShowroomFilter, ShowroomToCustomerFilter
from src.transaction.serializers import FromDealerToShowroomTransactionSerializer, \
    FromShowroomToCustomerTransactionSerializer
from src.transaction.models import FromDealerToShowroomTransaction, FromShowroomToCustomerTransaction


class FromDealerToShowroomTransactionView(GenericViewSet):
    """
    View information about Dealer-Showroom Transactions
    """

    queryset = FromDealerToShowroomTransaction.objects.all()
    serializer_class = FromDealerToShowroomTransactionSerializer
    permission_classes = [(IsDealerUser | IsShowroomUser | IsAdminUser)]
    filterset_class = DealerToShowroomFilter

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            transactions = FromDealerToShowroomTransaction.objects.all()
            serializer = self.get_serializer(transactions, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.is_dealer:
            transactions = FromDealerToShowroomTransaction.objects.filter(dealer=self.request.user.dealer)
            serializer = self.get_serializer(transactions, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.is_showroom:
            transactions = FromDealerToShowroomTransaction.objects.filter(showroom=self.request.user.showroom)
            serializer = self.get_serializer(transactions, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.request.user.is_superuser:
            transaction = FromDealerToShowroomTransaction.objects.get(id=pk)
            serializer = self.get_serializer(transaction, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.is_dealer:
            transaction = FromDealerToShowroomTransaction.objects.get(id=pk)
            if transaction.dealer == request.user.dealer:
                serializer = self.get_serializer(transaction, many=False)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': "You see this because you are not the participant in this transaction"},
                                status=status.HTTP_403_FORBIDDEN)
        elif self.request.user.is_showroom:
            transaction = FromDealerToShowroomTransaction.objects.get(id=pk)
            if transaction.showroom == request.user.showroom:
                serializer = self.get_serializer(transaction, many=False)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': "You see this because you are not the participant in this transaction"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


class FromShowroomToCustomerTransactionView(GenericViewSet):
    """
    View information about Showroom-Customer Transactions
    """

    queryset = FromShowroomToCustomerTransaction.objects.all()
    serializer_class = FromShowroomToCustomerTransactionSerializer
    permission_classes = [(IsCustomerUser | IsShowroomUser | IsAdminUser)]
    filterset_class = ShowroomToCustomerFilter

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            transactions = FromShowroomToCustomerTransaction.objects.all()
            serializer = self.get_serializer(transactions, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.is_showroom:
            transactions = FromShowroomToCustomerTransaction.objects.filter(showroom=self.request.user.showroom)
            serializer = self.get_serializer(transactions, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.is_customer:
            transactions = FromShowroomToCustomerTransaction.objects.filter(customer=self.request.user.customer)
            serializer = self.get_serializer(transactions, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.request.user.is_superuser:
            transaction = FromShowroomToCustomerTransaction.objects.get(id=pk)
            serializer = self.get_serializer(transaction, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        elif self.request.user.is_showroom:
            transaction = FromShowroomToCustomerTransaction.objects.get(id=pk)
            if transaction.showroom == request.user.showroom:
                serializer = self.get_serializer(transaction, many=False)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': "You see this because you are not the participant in this transaction"},
                                status=status.HTTP_403_FORBIDDEN)
        elif self.request.user.is_customer:
            transaction = FromShowroomToCustomerTransaction.objects.get(id=pk)
            if transaction.customer == request.user.customer:
                serializer = self.get_serializer(transaction, many=False)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': "You see this because you are not the participant in this transaction"},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
