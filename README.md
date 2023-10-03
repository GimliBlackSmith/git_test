# ip_manager
#Task2

Работа веб-приложения:

create/<str:network_address>/<str:network_prefix> - выделить сеть

delete/<str:network_uuid> - удалить сеть

allocate/<str:network_address>/<str:network_prefix> - выделить адрес в указанной сети

deallocate/<str:dedicated_address_uuid> - отменить выделение адреса

dedicated_addreses/ - получить список выделенных адресов
