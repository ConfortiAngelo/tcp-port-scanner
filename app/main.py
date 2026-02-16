from utils.validators import validator_port_target, validator_ip_target
from utils.exceptions import ScannerError

def main():
    print("Inicio del programa")

    try:
        validator_ip_target("192.2.2.0/24")
        validator_port_target([20,21,443,80,[20,80]])
    except ScannerError as e:
        print(f"[ERROR] {e}")
        return

    print("Fin del programa")

if __name__ == "__main__":
    main()
