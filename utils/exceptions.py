class ScannerError(Exception):
    pass


#IPS
class InvalidIPError(ScannerError):
    pass
class InvalidIPRangeError(ScannerError):
    pass
class InvalidPortError(ScannerError):
    pass
class ScanConfigurationError(ScannerError):
    pass