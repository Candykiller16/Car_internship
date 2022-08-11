from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsShowroomUser, IsCustomerUser
from src.showroom.filters import ShowroomFilter
from src.showroom.models import Showroom
from src.showroom.serializers import ShowroomSerializer


class ShowroomViewSet(mixins.RetrieveModelMixin,
                      GenericViewSet):
    """
    Viewset to see information about Showrooms
    """
    queryset = Showroom.objects.all()
    serializer_class = ShowroomSerializer
    permission_classes = [(IsAdminUser | IsShowroomUser | IsCustomerUser)]
    filterset_class = ShowroomFilter
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name",)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_customer:
            showroom = Showroom.objects.all()
            serializer = self.get_serializer(showroom, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None, *args, **kwargs):
        if self.request.user.is_superuser or self.request.user.is_customer:
            serializer = self.get_serializer(Showroom.objects.get(id=pk))
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request, *args, **kwargs):
        if request.user.is_showroom:
            showroom = self.request.user.showroom
            if request.method == 'GET':
                serializer = self.get_serializer(showroom)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            elif request.method == 'PUT':
                serializer = self.get_serializer(showroom, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk=None):
        if request.user.is_superuser:
            showroom = self.get_object()
            serializer = self.get_serializer(showroom, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"showroom": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
