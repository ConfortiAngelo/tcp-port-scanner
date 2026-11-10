"""Integration tests: scan sockets opened by the test itself on 127.0.0.1 only."""

from core.models import PortStatus
from core.scanner import scanner


def test_open_port_with_banner(ssh_like_server):
    [host] = scanner(["127.0.0.1"], [ssh_like_server])
    [result] = host.port_result
    assert result.status is PortStatus.OPEN
    assert result.banner.startswith("SSH-2.0-")


def test_closed_port(closed_port):
    [host] = scanner(["127.0.0.1"], [closed_port])
    assert host.port_result[0].status is PortStatus.CLOSED


def test_summary_counts(ssh_like_server, closed_port):
    [host] = scanner(["127.0.0.1"], [ssh_like_server, closed_port])
    assert host.summary() == {"open": 1, "closed": 1, "filtered": 0}
