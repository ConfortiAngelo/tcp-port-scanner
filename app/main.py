from utils.validators import validator_ip , validator_port , validator_port_target
from utils.exceptions import ScannerError

def main():
    print("Inicio del programa")

    try:
#        validator_ip("192.168.1.0/24")
#        validator_port(80233)
        validator_port_target([20,21,443,80,[20,80000]])
    except ScannerError as e:
        print(f"[ERROR] {e}")
        return

    print("Fin del programa")

if __name__ == "__main__":
    main()
