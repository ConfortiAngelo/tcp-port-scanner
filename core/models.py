from dataclasses import dataclass , field
from enum import Enum
from ipaddress import IPv4Address , IPv6Address

class PortStatus(Enum):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    FILTERED = 'FILTERED'

class ScanType(Enum):
    TCP_CONNECT = 'tcp connect'
    TCP_SYN = 'tcp syn'

@dataclass
class PortScanResult:
    #ip : IPv4Address | IPv6Address
    ip : str
    port : int
    status : PortStatus
    scan_type : ScanType
    banner : str | None = None
    durations_ms : float | None = None

@dataclass
class HostScanResult:
    #ip : IPv4Address | IPv6Address
    ip : str
    port_result : list[PortScanResult] = field(default_factory = list)
    total_duration_ms : float | None = None

    def open_port(self):
        return [r for r in self.port_result if r.status == PortStatus.OPEN]
    
    def summary(self):
        return {
            "open" : sum(1 for r in self.port_result if r.status == PortStatus.OPEN),
            "closed" : sum(1 for r in self.port_result if r.status == PortStatus.CLOSED),
            "filtered" : sum(1 for r in self.port_result if r.status == PortStatus.FILTERED)
        }   