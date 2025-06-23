from django.contrib import admin

from .models import Delivery, DeliveryStatus, PackagingType, Service, TransportModel

admin.site.register([Delivery, DeliveryStatus, PackagingType, Service, TransportModel])
