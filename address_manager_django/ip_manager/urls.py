from django.urls import path
from . import views
   
urlpatterns = [
    path('', views.index, name='index'),
   
    path('create/<str:network_address>/<str:network_prefix>',
         views.new_network,
         name='new_network_path'),

    path('delete/<str:network_uuid>',
         views.delete_network,
         name='delete_network_path'),

    path('allocate/<str:network_address>/<str:network_prefix>',
         views.allocate_dedicated_address,
         name='allocate_dedicated_address_path'),

    path('deallocate/<str:dedicated_address_uuid>',
         views.deallocate_dedicated_address,
         name='deallocate_dedicated_address_path'),
    
    path('dedicated_addreses/',
         views.all_dedicated_adreses,
         name='dedicated_addreses_path'),
    
    path('delete_all/',
         views.delete_all_addresses,
         name='delete_all_path'),
    
]