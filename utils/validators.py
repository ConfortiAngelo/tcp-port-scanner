from cgi import print_arguments
import ipaddress
from utils.exceptions import InvalidIPError, InvalidIPRangeError , InvalidPortError , InvalidPortRangeError
from utils.target_resolver import generate_ip_range

def validator_ip(address : str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:  
    try:        
        ip = ipaddress.ip_address(address) 
        return ip 
    except ValueError:
        raise InvalidIPError(f'IP : {address} invalida ')

def validator_ip_network(address : str)-> ipaddress.IPv4Address | ipaddress.IPv6Address: 
    try:
        ip = ipaddress.ip_network(address, strict=False)
        generate_ip_range(ip)
    except ValueError:
        raise InvalidIPRangeError(f'Rango : {address} es invalido')

def validator_ip_target(address : str)-> ipaddress.IPv4Address | ipaddress.IPv6Address: 
    if '/' in address:
        return validator_ip_network(address)
    else:
        return validator_ip(address)

def validator_port(port : int):
    if not 1 <= port <= 65535:
        raise InvalidPortError(f'Puerto : {port} invalido')
    else:
        return port


def validator_port_target(ports:list):
    list_ports = []
    for item in ports:
        if isinstance(item , int):
            port_unique = validator_port(item)
            list_ports.append(port_unique)
        elif isinstance(item , list):
            if len(item) == 2 and (item[0] < item[1]):
                for port in range(item[0],item[1]+1):
                    port_range = validator_port(port)
                    list_ports.append(port_range)
            else :
                raise InvalidPortRangeError(f'Rango de puertos invalido')
            
    return list_ports

            
                


            

    
