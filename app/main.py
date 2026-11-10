import argparse
import sys
from utils.exceptions import ScannerError
from config.settings import DEFAULT_PORT_RANGE,INFO_LVL
from core.ports import validator_port_target , convert_port
from utils.validators import validator_ip_target
from core.scanner import scanner
from utils.output import render_host_result


def main():
    #Parsear datos
    parser = argparse.ArgumentParser(prog='scanner',description='TCP port scan',epilog='python -m app.main -t 127.0.0.1 -p 22 80 [8000,8100]')
    parser.add_argument('-t','--target',nargs='+',type=str,required=True,help='IPs destino')
    parser.add_argument('-p','--port',nargs='+',type=str,help='Puerto/s a escanear. -p 22 80 443',default=None)
    args = parser.parse_args()

    #Validaciones de datos
    try:
        ports = validator_port_target(convert_port(args.port if args.port is not None else DEFAULT_PORT_RANGE.copy()))
        targets = validator_ip_target(args.target)
    except (ScannerError, ValueError) as e:
        print(f'[ERROR] {e}', file=sys.stderr)
        sys.exit(2)

    target_list = []
    for target in targets:
        if isinstance(target,list):
            for ip in target:
                target_list.append(ip)
        else:
            target_list.append(target)

    #Inicio de scaneo
    scanners = scanner(target_list,ports)

    #Mostrar datos al Usuario
    render_host_result(scanners)


if __name__ == "__main__":
    main()
