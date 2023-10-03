from django.contrib import admin

from .models import Network, DedicatedAddreses


#Определение доступа к классам таблиц
admin.site.register(Network)
admin.site.register(DedicatedAddreses)
