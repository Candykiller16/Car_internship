from django.urls import path, include
from rest_framework import routers

from src.customer.views import CustomerViewSet, CustomerOfferViewSet

router = routers.DefaultRouter()
router.register(r"customer", CustomerViewSet, basename="customer")
# router.register(r"customer_owner", CustomerOwnerViewSet, basename="customer-owner")
router.register(r"customer_offer", CustomerOfferViewSet, basename="customer_offer")

urlpatterns = [
    path("", include(router.urls)),
    # path("customer/offer/<int:pk>", CustomerOffersListApiView.as_view()),

]
