import asyncio
from core.models import HostScanResult
from infrastructure.async_executor import async_executor
from utils.logger import setup_logger
from config.settings import ERROR_LVL , INFO_LVL

def scanner(targets : list ,ports : list) -> list[HostScanResult]:
    if not isinstance(targets,list):
            targets = [targets]
    
    logger = setup_logger(INFO_LVL)
    logger.info('scan started ->',extra={'ip_target' : {str(targets)} , 'port_target' : {str(ports)}})
    try: 
        hostscanresult = asyncio.run(async_executor(targets,ports))
    except RuntimeError:
        logger = setup_logger(ERROR_LVL)
        logger.error('',extra={'cause' : 'RuntimeError' , 'failed' : 'Timeout'})
    

    return hostscanresult