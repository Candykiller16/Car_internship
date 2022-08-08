from django.urls import include, path
from rest_framework import routers

from src.showroom.views import ShowroomViewSet

router = routers.DefaultRouter()
router.register(r"showroom", ShowroomViewSet, basename="showroom")
urlpatterns = [
    path("", include(router.urls)),
]
