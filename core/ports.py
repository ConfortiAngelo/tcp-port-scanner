from utils.exceptions import InvalidPortError, InvalidPortRangeError

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




    