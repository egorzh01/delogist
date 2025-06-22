# Create your views here.
from django.db.models.query import QuerySet
from rest_framework import viewsets

from .models import Delivery, Service
from .serializers import (
    DeliverySerializer,
    ServiceSerializer,
)


class DeliveryViewSet(viewsets.ModelViewSet[Delivery]):
    http_method_names = ["get"]
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def get_queryset(self) -> QuerySet[Delivery]:
        qs = super().get_queryset()

        arrival_time_from = self.request.query_params.get("arrival_time_from")
        if arrival_time_from:
            qs = qs.filter(arrival_time__gte=arrival_time_from)
        arrival_time_to = self.request.query_params.get("arrival_time_to")
        if arrival_time_to:
            qs = qs.filter(arrival_time__lte=arrival_time_to)
        service_id = self.request.query_params.get("service")
        if service_id:
            qs = qs.filter(services__id=service_id)

        return qs


class ServiceViewSet(viewsets.ModelViewSet[Service]):
    http_method_names = ["get"]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
