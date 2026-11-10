import ipaddress

import pytest

from core.ports import convert_port, validator_port_target
from utils.exceptions import InvalidIPError, InvalidPortError, InvalidPortRangeError
from utils.validators import validator_ip_target


def test_convert_single_ports_and_ranges():
    assert convert_port(["22", "80", "[8000,8002]"]) == [22, 80, [8000, 8002]]


def test_range_is_expanded():
    assert validator_port_target([22, [8000, 8002]]) == [22, 8000, 8001, 8002]


@pytest.mark.parametrize("bad", [0, 65536, -1])
def test_out_of_range_port_is_rejected(bad):
    with pytest.raises(InvalidPortError):
        validator_port_target([bad])


def test_reversed_range_is_rejected():
    with pytest.raises(InvalidPortRangeError):
        validator_port_target([[100, 10]])


def test_garbage_port_is_rejected():
    with pytest.raises(ValueError):
        convert_port(["http"])


def test_cidr_expands_to_hosts():
    hosts = validator_ip_target(["192.0.2.0/30"])[0]
    assert hosts == [ipaddress.ip_address("192.0.2.1"), ipaddress.ip_address("192.0.2.2")]


def test_invalid_ip_is_rejected():
    with pytest.raises(InvalidIPError):
        validator_ip_target(["999.1.1.1"])
