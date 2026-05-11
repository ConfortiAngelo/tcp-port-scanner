import asyncio
from core.models import  PortScanResult, PortStatus, ScanType
from config.settings import DEBUG_LVL
from utils.logger import setup_logger
from core.services import get_service
async def connection(ip,port ,timeout):
    loop = asyncio.get_running_loop()
    start_time = loop.time()
    logger = setup_logger(DEBUG_LVL)
    try :
        reader , writer = await asyncio.wait_for(asyncio.open_connection(ip,port),timeout)
        try:
            banner = await asyncio.wait_for(reader.read(1024),timeout)
            banner = banner.decode(errors="ignore").rstrip("\r\n")
        except asyncio.TimeoutError:
            banner = ''
        writer.close()
        await writer.wait_closed()
        end_time = loop.time()
        durations_ms = (end_time - start_time) * 1000 
        portscanresult_open = PortScanResult(ip,port,PortStatus.OPEN,ScanType.TCP_CONNECT,banner,durations_ms)
        service, detected = get_service(portscanresult_open.port, portscanresult_open.banner)

        logger.debug('Iniciando conexion TCP ->',extra={'action' : 'Create socket' , 'ip_port' : f'{ip}:{str(port)}','state' :f'OPEN', 'service' : f'{service}{detected if detected else ''}'})
        return  portscanresult_open
    except (ConnectionRefusedError, OSError, ConnectionResetError):
        end_time = loop.time()
        
        durations_ms = (end_time - start_time) * 1000 
        portscanresult_closed = PortScanResult(ip,port,PortStatus.CLOSED,ScanType.TCP_CONNECT,"",durations_ms)

        service, detected = get_service(portscanresult_closed.port, portscanresult_closed.banner)
        logger.debug('Iniciando conexion TCP ->',extra={'action' : 'Create socket' , 'ip_port' : f'{ip}:{str(port)}','state' :f'Closed', 'service' : f'{service}{detected if detected else ''}'})

        return portscanresult_closed

    except asyncio.TimeoutError:
        end_time = loop.time()
        
        durations_ms = (end_time - start_time) * 1000 
        portscanresult_filtered = PortScanResult(ip,port,PortStatus.FILTERED,ScanType.TCP_CONNECT,"",durations_ms)
        service, detected = get_service(portscanresult_filtered.port, portscanresult_filtered.banner)
        print(f'SERVICE : {service}   ---- DETECTED : {detected}')
        logger.debug('Iniciando conexion TCP ->',extra={'action' : 'Create socket' , 'ip_port' : f'{ip}:{str(port)}','state' :f'Filtered', 'service' : f'{service}{detected if detected else ''}'})

        return portscanresult_filtered

