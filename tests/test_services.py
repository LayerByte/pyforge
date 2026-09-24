from pyforge.services.exporter import export_csv, export_json, export_txt
from pyforge.storage.history import HistoryService


def test_history_records_lists_and_clears(tmp_path):
    service = HistoryService(tmp_path / "history.db")
    service.record("text.word-count", True, 1.25)
    assert service.list()[0]["tool"] == "text.word-count"
    assert service.clear() == 1 and service.list() == []


def test_history_try_record_tolerates_unavailable_storage(tmp_path):
    blocker = tmp_path / "blocker"
    blocker.write_text("not a directory", encoding="utf-8")
    service = HistoryService(blocker / "history.db")
    assert service.try_record("text.word-count", True, 1.25) is False


def test_exporters_write_supported_formats(tmp_path):
    data = [{"name": "ž", "count": 2}]
    assert "ž" in export_json(data, tmp_path / "x.json").read_text(encoding="utf-8")
    assert "name" in export_csv(data, tmp_path / "x.csv").read_text(encoding="utf-8")
    assert export_txt(data, tmp_path / "x.txt").read_text(encoding="utf-8").endswith("\n")
