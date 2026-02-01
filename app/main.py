from utils.validators import validator_ip
from utils.exceptions import ScannerError

def main():
    print("Inicio del programa")

    try:
        validator_ip("192.2.2.10123")
        print("IP válida, continuando escaneo...")
    except ScannerError as e:
        print(f"[ERROR] {e}")
        return

    print("Fin del programa")

if __name__ == "__main__":
    main()
