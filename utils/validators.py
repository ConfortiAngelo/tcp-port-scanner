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

def validator_ip_target(address : list)-> ipaddress.IPv4Address | ipaddress.IPv6Address: 
    validator = []
    for item in address:
        if '/' in item:
            validator.append(validator_ip_network(item))
        else:
            validator.append(validator_ip(item))
    return validator