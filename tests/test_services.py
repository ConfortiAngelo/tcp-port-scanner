from core.services import get_service


def test_banner_wins_over_port_number():
    assert get_service(2222, "SSH-2.0-OpenSSH_9.6") == ("ssh", True)


def test_well_known_port_without_banner():
    assert get_service(443, None) == ("https", None)


def test_unknown_port_without_banner():
    assert get_service(54321, None) == ("unknown", None)
