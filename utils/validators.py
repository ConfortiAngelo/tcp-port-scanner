import ipaddress
from utils.exceptions import InvalidIPError, InvalidIPRangeError , InvalidPortError

def validator_ip(address : str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:  
    try:        
        ip = ipaddress.ip_address(address)  
    except ValueError:
        raise InvalidIPError(f'IP : {address} invalida ')

def validator_ip_network(address : str)-> ipaddress.IPv4Address | ipaddress.IPv6Address: 
    try:
        ip = ipaddress.ip_network(address, strict=False)
    except ValueError:
        raise InvalidIPRangeError(f'Rango : {address} es invalido')

def validator_target(address : str)-> ipaddress.IPv4Address | ipaddress.IPv6Address: 
    if '/' in address:
        return validator_ip_network(address)
    else:
        return validator_ip(address)

def validator_port(port : int):
    if not 1 <= port <= 65535:
        raise InvalidPortError(f'Puerto : {port} invalido')
    else:
        print(f'Puerto : {port} valido')


# recibir una lista [....] y llamar a las funciones correspondientes
def validator_port_target(ports:list):
    for item in ports:
        if isinstance(item , int):
            validator_port(item)
        elif isinstance(item , list):
            for port in range(item[0],item[1]+1):
                validator_port(port)

            
                


            

    
