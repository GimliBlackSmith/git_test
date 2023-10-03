import logging

from django.http import HttpResponse
from django.shortcuts import render

from .models import Network, DedicatedAddreses
from .functions import generate_dedicate_addresses, check_network_format

logging.basicConfig(
    level=logging.INFO, filename="py_log.log",
    filemode="w", format="%(asctime)s %(levelname)s %(message)s")

def index(request):
    logging.info(f"Attempt to def index\n")
    
    # Рендеринг - процесс наполнения шаблона данными
    return render(request,'ip_manager/base.html')

def new_network(request, network_address, network_prefix):
    # Объединение адреса и префикса сети
    network_address += '/'
    network_address += network_prefix
    
    # Проверка корректности введённых данных
    network_is_correct = check_network_format(network_address)
    
    logging.info(f"(new_network)NETWORK_IS_CORRECT = {network_is_correct}\n")
    
    # Проверка существования сети в таблице
    network_allocated = Network.objects\
        .filter(network_address = network_address)\
            .exists()
            
    logging.info(f"(new_network)NETWORK_ALLOCATED = {network_allocated}\n")
    
    if network_is_correct:
        if network_allocated:
            
            return HttpResponse("This network is already create.")

        else:     
            try:   
                logging.info(f"ATTEMPT to add new network_address ="
                             f"{type(network_address)}\n")
                # Добавляем кортеж в таблицу       
                Network.objects\
                    .get_or_create(network_address = network_address)
                # Генератор выделенных адресов сети
                generate_dedicate_addresses(network_address)
                
                query_results  = Network.objects\
                    .filter(network_address = network_address)
                    
                logging.info(f"query_results = {query_results}\n")
                logging.info(f"query_results = {type(query_results)}\n")
                
                # Определение вывода (заполняем контекст)
                context = {'query_results': query_results,}
                
                return render(request, 'ip_manager/view_result.html', context)

            except Exception as error:
                logging.info(f"FAILED to add new_network = "
                             f"{network_address}\n"
                             f"(new_network)ERROR: {error}")
                
                return HttpResponse(f"You're NOT add network: " 
                                    f"{network_address}\n"
                                    f"(new_network)ERROR: {error}")
            
    else:
        
        return HttpResponse("This network address is't correct.")
    
def delete_network(request, network_uuid):
    # Проверка существования сети в таблице
    network_allocated = Network.objects\
        .filter(uuid = network_uuid)\
            .exists()
            
    logging.info(f"network_allocated = "
                 f"{network_allocated}\n")
    
    if network_allocated:
        try:
            Network.objects\
                .filter(uuid = network_uuid)\
                    .delete()
                    
            logging.info(f"Attempt to delete_network with uuid = "
                         f"{network_uuid}\n")
            
            return HttpResponse("You're delete network.")
        
        except Exception as error:
            logging.info(f"Failed to delete_network ="
                         f"{network_uuid}\n"
                         f"(delete_network)Error: {error}")    
            
            return HttpResponse("You're not delete network with uuid %s = " 
                                f"{network_uuid}\n"
                                f"(delete_network)Error: {error}")
        
    else:
        
        return HttpResponse("You're not delete network with uuid %s = " 
                            f"{network_uuid}\n")

def allocate_dedicated_address(request, network_address, network_prefix):
    # Объединение адреса и префикса сети
    network_address += '/'
    network_address += network_prefix
    
    # Проверка существования сети в таблице
    network_allocated = Network.objects\
        .filter(network_address = network_address)\
            .exists()
    
    logging.info(f"network_allocated = "
                 f"{network_allocated}\n")
    
    if network_allocated:
        try:
            
            logging.info(f"Attempt to allocate_dedicated_address = "
                         f"{network_address}\n")
            
            # Возвращает id
            dedicated_adress_id = DedicatedAddreses.objects\
                .filter(network_address = network_address, avaible = 'YES')\
                    .values_list('id')[0]
                   
            logging.info(f"dedicated_adress_id = "
                         f"{dedicated_adress_id[0]}\n")
            logging.info(f"dedicated_adress_id = "
                         f"{type(dedicated_adress_id[0])}\n")
            
            # Обновляет значение поля "Avaible" на "NO", т.е. адрес выделен
            DedicatedAddreses.objects\
                .filter(id = dedicated_adress_id[0])\
                    .update(avaible = 'NO')

            #Выводит правильный выделенный адрес?
            query_results  = DedicatedAddreses.objects\
                .filter(id = dedicated_adress_id[0])
                    
            logging.info(f"dedicated_adress_id = "
                         f"{type(query_results)}\n")
            logging.info(f"dedicated_adress_id = "
                         f"{query_results}\n")
            
            #Определение вывода (заполняем контекст)
            context = {'dedicated_query_results': query_results,}
            
            return render(request, 'ip_manager/view_result.html', context)
        
        except Exception as error:
            logging.info("ATTEMPT to ALLOCATE_DEDICATED_ADDRESS %s :"
                         f"{network_address}\n"
                         f"(allocate_dedicated_address)ERROR: {error}")
          
            return HttpResponse("FAILED to allocate_dedicated_address %s:"
                                f"{network_address}\n"
                                f"(allocate_dedicated_address)ERROR: {error}")
        
    else:
        
        return HttpResponse("You're not allocate network with network_address %s:" 
                            f"{network_address}\n")


def deallocate_dedicated_address(request, dedicated_address_uuid):
    # Проверка существования сети в таблице
    network_allocated = DedicatedAddreses.objects\
        .filter(dedicated_uuid = dedicated_address_uuid, avaible = 'NO' )\
            .exists()
    
    logging.info(f"network_allocated = {network_allocated}\n")
    
    if network_allocated: 
        try:
            logging.info("Attempt to deallocate_dedicated_address %s = "
                         f"{dedicated_address_uuid}\n")
        
            DedicatedAddreses.objects\
                .filter(dedicated_uuid = dedicated_address_uuid)\
                    .update(avaible = 'YES') 
            
            return HttpResponse("You're deallocate dedicated_address.")
        
        except Exception as error:
            logging.info("FAILED to DEALLOCATE_DEDICATED_ADDRESS %s = "
                         f"{dedicated_address_uuid}\n"
                         f"(deallocate_dedicated_address)ERROR: {error}")
            
            return HttpResponse(f"You're NOT DEALLOCATE_DEDICATED_ADDRESS"
                                f"with address: " 
                                f"{dedicated_address_uuid}\n" 
                                f"(deallocate_dedicated_address)Error: {error}")
    
    else:
        
        return HttpResponse("You're NOT deallocate_dedicated_address with uuid %s:" 
                            f"{dedicated_address_uuid}\n")

def all_dedicated_adreses(request):
    query_results  = DedicatedAddreses.objects\
        .filter(avaible = 'NO')
            
        
    logging.info(f"All_dedicated_adreses = {query_results}\n")
    logging.info(f"All_dedicated_adreses = {type(query_results)}\n")
        
    # Определение вывода (заполняем контекст)    
    context = {'dedicated_query_results': query_results,}
    
    return render(request, 'ip_manager/view_result.html', context)


def delete_all_addresses(request):
    DedicatedAddreses.objects\
        .all().delete()
        
    Network.objects\
        .all().delete()

    return HttpResponse("All tables are clean.")