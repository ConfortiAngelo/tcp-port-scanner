from utils.exceptions import InvalidPortError, InvalidPortRangeError

def convert_port(ports : list):
    ports_converts = []
    for item in ports:
        if item.isdigit():
            ports_converts.append(int(item))
        elif item.startswith('[') and item.endswith(']'):
            try:
                start,end = item[1:-1].split(',')
                ports_converts.append([int(start),int(end)])
            except:
                raise ValueError(f'Formato invalido : {item}')
        else:
            raise ValueError(f"Entrada no válida: {item}")
    return ports_converts

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




    