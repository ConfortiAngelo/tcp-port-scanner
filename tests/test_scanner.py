from utils.validators import  validator_ip_target
from core.ports import validator_port_target
from utils.exceptions import ScannerError
from config.settings import DEFAULT_PORT_RANGE , INFO_LVL , DEBUG_LVL, WARNING_LVL, ERROR_LVL
from utils.logger import setup_logger
from core.models import PortStatus, PortScanResult, HostScanResult , ScanType
from infrastructure.scoket_client import connection
from infrastructure.async_executor import async_executor
from core.scanner import scanner
import asyncio
from utils.output import render_host_reuslt

def main():
    print("Inicio del programa")
    try:
        data_ip = validator_ip_target("192.2.2.0/29")
        data_port =  validator_port_target([10,11,[22,30]])
        print(f'IP : {data_ip} \nPorts :< \n{data_port}')
        logger = setup_logger(INFO_LVL)  
        logger.info('scan started ->',extra={'ip_target' : "10.23.232.2" , 'port_target' : "100" , 'threads' : 100})
        logger = setup_logger(DEBUG_LVL)
        logger.debug('',extra={'action' : 'Create socket' , 'ip_port' : "10.23.232.2:100", "timeout" : '1s'})
        logger.debug('',extra={'action' : "Thread-12 starting"})
        logger = setup_logger(ERROR_LVL)
        logger.error('',extra={'cause' : 'Timeout exceeded' , 'failed' : '10.23.232.2:100'})
        
        portstatus = PortStatus("OPEN")
        scantype = ScanType("tcp connect")

        portscanresult = PortScanResult(ip="10.23.232.2", port=22,status= portstatus,scan_type=scantype,banner=None,durations_ms=1.232)
        hostscanresult = HostScanResult(ip="10.23.232.2",port_result= [portscanresult],total_duration_ms= 2.323)    


        print('--'*20)
 #       print(asyncio.run(connection('192.168.56.101',50,2)))
        print('--'*20)
#        print(asyncio.run(async_executor(data_ip,[1,22])))
        print('--'*20)
        scanners = scanner(data_ip,[1,22,443,8080,80,21])
        print(scanners)
        print('--'*20)
        #render_header(scanners)
        #render_scan_info(scanners)
        #render_ports_table(scanners)
        #host_summary(scanners)
        #final_host_summary(scanners)
        render_host_reuslt(scanners)
    except ScannerError as e:
        print(f"[ERROR] {e}")
        return

    print("Fin del programa")

if __name__ == "__main__":
    main()
