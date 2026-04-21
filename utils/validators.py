import ipaddress
from utils.exceptions import InvalidIPError, InvalidIPRangeError
from utils.target_resolved import generate_ip_range

def validator_ip(address : str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:  
    try:        
        ip = ipaddress.ip_address(address) 
        return ip 
    except ValueError:
        raise InvalidIPError(f'IP : {address} invalida ')

def validator_ip_network(address : str)-> ipaddress.IPv4Address | ipaddress.IPv6Address: 
    try:
        ip = ipaddress.ip_network(address, strict=False)
        range_ip = generate_ip_range(ip)
        return range_ip
    except ValueError:
        raise InvalidIPRangeError(f'Rango : {address} es invalido')

def validator_ip_target(address : str)-> ipaddress.IPv4Address | ipaddress.IPv6Address: 
    if '/' in address:
        return validator_ip_network(address)
    else:
        return validator_ip(address)


            
                


            

    
