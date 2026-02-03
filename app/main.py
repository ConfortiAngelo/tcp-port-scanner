from utils.validators import validator_ip , validator_port
from utils.exceptions import ScannerError

def main():
    print("Inicio del programa")

    try:
        validator_ip("192.2.2.10")
        validator_port(80)
    except ScannerError as e:
        print(f"[ERROR] {e}")
        return

    print("Fin del programa")

if __name__ == "__main__":
    main()
