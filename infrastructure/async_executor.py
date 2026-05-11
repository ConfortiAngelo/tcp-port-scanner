import asyncio
from infrastructure.scoket_client import connection
from core.models import HostScanResult, PortScanResult
from config.settings import DEFAULT_TASK , DEFAULT_TIMEOUT, ERROR_LVL, DEBUG_LVL
from utils.logger import setup_logger

async def executor(ip : str,port : int, limited) -> PortScanResult:
    async with limited:
        return await connection(ip,port,DEFAULT_TIMEOUT)


async def async_executor(ips : list ,ports : list) -> list[HostScanResult]:
    loop = asyncio.get_running_loop()
    limited = asyncio.Semaphore(DEFAULT_TASK)
    hosts_results = []

    for ip in ips:
        start_time = loop.time()
        ip_str = str(ip)
        tasks = []
        try :
            async with asyncio.TaskGroup() as tg:  
                for port in ports:
                    task = tg.create_task(executor(ip_str,port,limited))
                    tasks.append(task)
            ports_results = [task.result() for task in tasks]
        except* OSError as eg:
            logger = setup_logger(ERROR_LVL)
            logger.error('',extra={'cause' : 'Network Error' , 'failed' : {ip_str}})
            ports_results = []
        
        total_duration_ms = (loop.time() - start_time)*1000
        hosts_results.append(HostScanResult(ip_str, ports_results, total_duration_ms))    
        
    return hosts_results


