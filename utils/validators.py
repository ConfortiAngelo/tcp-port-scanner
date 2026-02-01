import ipaddress
from utils.exceptions import InvalidIPError , InvalidPortError

def validator_ip(address):
    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        raise InvalidIPError(f'IP invalida : {address}')



