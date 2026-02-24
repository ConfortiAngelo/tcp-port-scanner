from utils.validators import validator_port_target, validator_ip_target
from utils.exceptions import ScannerError
from config.settings import DEFAULT_PORT_RANGE
from utils.logger import setup_logger

def main():
    print("Inicio del programa")
    try:
        logger = setup_logger(20)
        logger.info('scan started')
        logger.warning('scan warning')
        validator_ip_target("192.2.2.0/24")

        data =  validator_port_target(DEFAULT_PORT_RANGE)
        print(data)
    except ScannerError as e:
        print(f"[ERROR] {e}")
        return

    print("Fin del programa")

if __name__ == "__main__":
    main()
