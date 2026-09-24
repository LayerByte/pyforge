def test_dns_lookup_deduplicates_resolver_results(monkeypatch):
    from pyforge.tools.network.core import dns_lookup

    monkeypatch.setattr("socket.getaddrinfo", lambda *_: [(2, 1, 6, "", ("1.2.3.4", 0)), (2, 1, 6, "", ("1.2.3.4", 0))])
    assert dns_lookup("example.test") == ["1.2.3.4"]


def test_reverse_dns_validates_address(monkeypatch):
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.network.core import reverse_dns_lookup

    monkeypatch.setattr("socket.gethostbyaddr", lambda value: ("host.test", [], [value]))
    assert reverse_dns_lookup("127.0.0.1") == "host.test"
    with pytest.raises(ValidationError):
        reverse_dns_lookup("999.1.1.1")


def test_local_ip_information_has_hostname(monkeypatch):
    from pyforge.tools.network.core import local_ip_information

    monkeypatch.setattr("socket.gethostname", lambda: "devbox")
    monkeypatch.setattr("socket.getaddrinfo", lambda *_: [(2, 1, 6, "", ("10.0.0.2", 0))])
    assert local_ip_information() == {"hostname": "devbox", "addresses": ["10.0.0.2"]}


def test_network_interfaces_combines_addresses_and_state(monkeypatch):
    from collections import namedtuple
    from pyforge.tools.network.core import network_interfaces

    Addr = namedtuple("Addr", "family address netmask broadcast ptp")
    Stat = namedtuple("Stat", "isup duplex speed mtu flags", defaults=[""])
    monkeypatch.setattr("psutil.net_if_addrs", lambda: {"lo": [Addr(2, "127.0.0.1", "255.0.0.0", None, None)]})
    monkeypatch.setattr("psutil.net_if_stats", lambda: {"lo": Stat(True, 0, 0, 0, "")})
    assert network_interfaces()[0]["up"] is True


def test_public_ip_uses_bounded_http_client():
    import httpx
    from pyforge.tools.network.core import public_ip

    client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={"ip": "203.0.113.5"}))
    )
    try:
        assert public_ip(client=client) == "203.0.113.5"
    finally:
        client.close()


def test_http_headers_rejects_non_http_and_reads_response():
    import httpx, pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.network.core import http_headers

    client = httpx.Client(
        transport=httpx.MockTransport(lambda request: httpx.Response(200, headers={"server": "test"}))
    )
    try:
        assert http_headers("https://example.test", client=client)["server"] == "test"
    finally:
        client.close()
    with pytest.raises(ValidationError):
        http_headers("file:///tmp/x")


def test_http_status_reports_success():
    import httpx
    from pyforge.tools.network.core import http_status

    client = httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(204)))
    try:
        result = http_status("https://example.test", client=client)
        assert result["status"] == 204 and result["ok"]
    finally:
        client.close()


def test_url_parser_extracts_components():
    from pyforge.tools.network.core import parse_url

    result = parse_url("https://example.test:8443/a?q=1#x")
    assert result["port"] == 8443 and result["path"] == "/a" and result["query"] == "q=1"
