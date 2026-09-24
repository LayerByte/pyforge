def test_cpu_information_has_counts(monkeypatch):
    from pyforge.tools.system.core import cpu_information

    monkeypatch.setattr("psutil.cpu_count", lambda logical=True: 8 if logical else 4)
    monkeypatch.setattr("psutil.cpu_percent", lambda interval: 12.5)
    monkeypatch.setattr("psutil.cpu_freq", lambda: None)
    result = cpu_information()
    assert result["physical_cores"] == 4 and result["logical_cores"] == 8


def test_memory_information_maps_psutil_values(monkeypatch):
    from types import SimpleNamespace
    from pyforge.tools.system.core import memory_information

    monkeypatch.setattr("psutil.virtual_memory", lambda: SimpleNamespace(total=10, available=4, used=6, percent=60))
    monkeypatch.setattr("psutil.swap_memory", lambda: SimpleNamespace(total=2, used=1, percent=50))
    assert memory_information()["available"] == 4


def test_disk_information_skips_inaccessible_mounts(monkeypatch):
    from types import SimpleNamespace
    from pyforge.tools.system.core import disk_information

    monkeypatch.setattr(
        "psutil.disk_partitions", lambda all=False: [SimpleNamespace(device="d", mountpoint="/x", fstype="x")]
    )
    monkeypatch.setattr("psutil.disk_usage", lambda path: SimpleNamespace(total=10, used=3, free=7, percent=30))
    assert disk_information()[0]["free"] == 7


def test_operating_system_information_has_platform():
    from pyforge.tools.system.core import operating_system_information

    result = operating_system_information()
    assert result["system"] and result["platform"]


def test_environment_information_redacts_sensitive_values(monkeypatch):
    from pyforge.tools.system.core import environment_information

    monkeypatch.setenv("PYFORGE_TEST_TOKEN", "private")
    monkeypatch.setenv("PYFORGE_VISIBLE", "ok")
    result = environment_information()
    assert result["PYFORGE_TEST_TOKEN"] == "[REDACTED]" and result["PYFORGE_VISIBLE"] == "ok"


def test_process_viewer_applies_limit(monkeypatch):
    from types import SimpleNamespace
    from pyforge.tools.system.core import process_viewer

    monkeypatch.setattr(
        "psutil.process_iter",
        lambda fields: [
            SimpleNamespace(info={"pid": 1, "memory_percent": 1}),
            SimpleNamespace(info={"pid": 2, "memory_percent": 5}),
        ],
    )
    assert process_viewer(1)[0]["pid"] == 2


def test_listening_ports_filters_connection_state(monkeypatch):
    from types import SimpleNamespace
    from pyforge.tools.system.core import listening_ports

    address = SimpleNamespace(ip="127.0.0.1", port=8080)
    monkeypatch.setattr(
        "psutil.net_connections",
        lambda kind: [
            SimpleNamespace(status="LISTEN", laddr=address, pid=1, family=2),
            SimpleNamespace(status="ESTABLISHED", laddr=address, pid=2, family=2),
        ],
    )
    assert listening_ports() == [{"address": "127.0.0.1", "port": 8080, "pid": 1, "family": "2"}]


def test_system_uptime_calculates_nonnegative_duration(monkeypatch):
    import time
    from pyforge.tools.system.core import system_uptime

    monkeypatch.setattr("psutil.boot_time", lambda: time.time() - 3661)
    result = system_uptime()
    assert result["seconds"] >= 3660 and result["hours"] == 1


def test_python_environment_information_reports_interpreter():
    from pyforge.tools.system.core import python_environment_information

    result = python_environment_information()
    assert result["executable"] and isinstance(result["path"], list)
