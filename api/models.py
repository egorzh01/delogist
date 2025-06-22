from django.db import models
from django_stubs_ext.db.models import TypedModelMeta


class TransportModel(models.Model):
    name = models.CharField(
        max_length=124,
        db_comment="Название модели",
    )

    class Meta(TypedModelMeta):
        db_table = "transport_models"
        verbose_name = "transport model"
        verbose_name_plural = "transport models"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class PackagingType(models.Model):
    name = models.CharField(
        max_length=124,
        db_comment="Название типа упаковки",
    )

    class Meta(TypedModelMeta):
        db_table = "packaging_types"
        verbose_name = "packaging type"
        verbose_name_plural = "packaging types"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Service(models.Model):
    name = models.CharField(
        max_length=124,
        db_comment="Название услуги",
    )

    class Meta(TypedModelMeta):
        db_table = "services"
        verbose_name = "service"
        verbose_name_plural = "services"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class DeliveryStatus(models.Model):
    name = models.CharField(
        max_length=124,
        db_comment="Название статуса",
    )
    color = models.CharField(
        max_length=7,
        null=True,
        db_comment="Цвет",
    )  # hex, e.g., "#00ff00"

    class Meta(TypedModelMeta):
        db_table = "delivery_statuses"
        verbose_name = "delivery status"
        verbose_name_plural = "delivery statuses"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="unique_delivery_status_name",
            )
        ]

    def __str__(self) -> str:
        return self.name


class Delivery(models.Model):
    transport_model = models.ForeignKey(
        TransportModel,
        on_delete=models.PROTECT,
        db_comment="Тип транспорта",
    )
    transport_number = models.CharField(
        max_length=64,
        db_comment="Номер транспорта",
    )
    departure_time = models.DateTimeField(
        db_comment="Время отправления",
    )
    arrival_time = models.DateTimeField(
        db_comment="Время прибытия",
    )
    distance_km = models.FloatField(
        db_comment="Расстояние в км",
    )
    file = models.FileField(
        upload_to="delivery_files/",
        null=True,
        blank=True,
        db_comment="Файл с информацией о доставке",
    )
    services = models.ManyToManyField(
        Service,
        db_table="deliveries_services",
        db_comment="Услуги",
    )
    status = models.ForeignKey(
        DeliveryStatus,
        on_delete=models.PROTECT,
        db_comment="Статус доставки",
    )
    packaging_type = models.ForeignKey(
        PackagingType,
        on_delete=models.PROTECT,
        db_comment="Тип упаковки",
    )
    tech_condition = models.CharField(
        max_length=10,
        choices=[("ok", "Исправно"), ("broken", "Неисправно")],
        db_comment="Техническое состояние",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_comment="Время создания",
    )

    class Meta(TypedModelMeta):
        db_table = "deliveries"
        verbose_name = "delivery"
        verbose_name_plural = "deliveries"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Delivery #{self.id}"
