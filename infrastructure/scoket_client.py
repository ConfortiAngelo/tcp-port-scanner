import asyncio
from core.models import  PortScanResult, PortStatus, ScanType
from config.settings import DEBUG_LVL
from utils.logger import setup_logger

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
        logger.debug('Iniciando conexion TCP ->',extra={'action' : 'Create socket' , 'ip_port' : f'{ip}:{str(port)}','state' :f'OPEN', 'service' : f'ssh'})
        return PortScanResult(ip,port,PortStatus.OPEN,ScanType.TCP_CONNECT,banner,durations_ms) 
    except (ConnectionRefusedError, OSError, ConnectionResetError):
        end_time = loop.time()
        logger.debug('Iniciando conexion TCP ->',extra={'action' : 'Create socket' , 'ip_port' : f'{ip}:{str(port)}','state' :f'Closed', 'service' : f'ssh'})
        durations_ms = (end_time - start_time) * 1000 
        portscanresult = PortScanResult(ip,port,PortStatus.CLOSED,ScanType.TCP_CONNECT,"",durations_ms)
        return portscanresult

    except asyncio.TimeoutError:
        end_time = loop.time()
        durations_ms = (end_time - start_time) * 1000 
        portscanresult = PortScanResult(ip,port,PortStatus.FILTERED,ScanType.TCP_CONNECT,"",durations_ms)

        return portscanresult 

