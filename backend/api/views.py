# Create your views here.
from datetime import UTC, datetime, timedelta

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
            try:  # noqa: SIM105
                qs = qs.filter(
                    arrival_time__gte=datetime.strptime(arrival_time_from, "%Y-%m-%d")
                    .astimezone(tz=UTC)
                    .replace(hour=0, minute=0, second=0)
                )
            except ValueError:
                pass
        arrival_time_to = self.request.query_params.get("arrival_time_to")
        if arrival_time_to:
            try:  # noqa: SIM105
                qs = qs.filter(
                    arrival_time__lt=(
                        datetime.strptime(arrival_time_to, "%Y-%m-%d").astimezone(
                            tz=UTC
                        )
                        + timedelta(days=1)
                    ).replace(hour=0, minute=0, second=0)
                )
            except ValueError:
                pass
        service_id = self.request.query_params.get("service")
        if service_id:
            qs = qs.filter(services__id=service_id)

        return qs


class ServiceViewSet(viewsets.ModelViewSet[Service]):
    http_method_names = ["get"]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
