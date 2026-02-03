import ipaddress
from utils.exceptions import InvalidIPError , InvalidPortError

def validator_ip(address):
    try:
        ip = ipaddress.ip_address(address)
        print(f'IP : {ip} valida ')        
    except ValueError:
        raise InvalidIPError(f'IP : {address} invalida ')



def validator_port(port):
    try:
        if port > 1 and port < 65535:
            print(f'Puerto : {port} valido ')
    except ValueError:
        raise InvalidPortError(f'Puerto : {port} invalido')

