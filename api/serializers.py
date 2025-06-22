from rest_framework import serializers

from .models import Delivery, DeliveryStatus, PackagingType, Service, TransportModel


class TransportModelSerializer(serializers.ModelSerializer[TransportModel]):
    class Meta:
        model = TransportModel
        fields = ["id", "name"]


class PackagingTypeSerializer(serializers.ModelSerializer[PackagingType]):
    class Meta:
        model = PackagingType
        fields = ["id", "name"]


class ServiceSerializer(serializers.ModelSerializer[Service]):
    class Meta:
        model = Service
        fields = ["id", "name"]


class DeliveryStatusSerializer(serializers.ModelSerializer[DeliveryStatus]):
    class Meta:
        model = DeliveryStatus
        fields = ["id", "name", "color"]


class DeliverySerializer(serializers.ModelSerializer[Delivery]):
    transport_model = TransportModelSerializer(read_only=True)
    packaging_type = PackagingTypeSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    status = DeliveryStatusSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = "__all__"
