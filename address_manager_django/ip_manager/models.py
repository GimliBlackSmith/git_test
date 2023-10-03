import logging
import ipaddress

from .models import DedicatedAddreses

# Генератор выделенных адресов сети
def generate_dedicate_addresses(network_address):
    try:
        logging.info(f"(generate_dedicate_addresses)"
                     f"ATTEMPT to generate_dedicate_addresses for = " 
                     f"{network_address}\n")

        address = network_address
        
        # Преобразование в тип IPAddress
        new_network = ipaddress.ip_network(address)
        
        logging.info(f"(generate_dedicate_addresses) num_addresses ="
                     f"{new_network.num_addresses}\n")
        logging.info(f"(generate_dedicate_addresses) new_network ="
                     f"{new_network}\n")
        
        # Перебор полезных адресов в сети
        for ip in new_network.hosts():
            # В цикле создаёт все возможные адреса подсети и заполняет ими бд
            logging.info(f"ip = {ip}\n")
            
            # Добавляет кортежи в таблицу
            DedicatedAddreses.objects\
                .create(
                    network_address = address, dedicated_address = ip)
            
        return True
            
    except Exception as error:
        logging.info(f"(generate_dedicate_addresses)"
                     f"FAILED to generate_sibnet_addresses for uuid ="
                     f"{network_address}\n"
                     f"(generate_dedicate_addresses) ERROR: {error}")
        
        return False
    
    
# Проверка корректности введённых данных    
def check_network_format(network_address):
    try:
        address = network_address
        
        #Преобразование в тип IPAddress
        new_network = ipaddress.ip_network(address)
        
        logging.info(f"(check_network_format)"
                     f"Complete to check_network_format for network_address =" 
                     f"{new_network}\n")
        
        return True
        
    except Exception as error:
        
        logging.info(f"(check_network_format)"
                     f"Failed to generate_sibnet_addresses for network_address ="
                     f"{network_address}\n"
                     f"(check_network_format)Error: {error}")
        
    return False