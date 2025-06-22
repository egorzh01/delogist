from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DeliveryViewSet,
    ServiceViewSet,
)

router = DefaultRouter()
router.register("deliveries", DeliveryViewSet)
router.register("services", ServiceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
