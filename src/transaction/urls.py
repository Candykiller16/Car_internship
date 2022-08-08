from django.urls import path, include
from rest_framework import routers

from src.transaction.views import FromDealerToShowroomTransactionView, FromShowroomToCustomerTransactionView

router = routers.DefaultRouter()
router.register(r"dealer_showroom", FromDealerToShowroomTransactionView, "FromDealerToShowroomTransaction")
router.register(r"showroom_customer", FromShowroomToCustomerTransactionView, "Public Shipper Transaction")

urlpatterns = [
    path("", include(router.urls)),
]
