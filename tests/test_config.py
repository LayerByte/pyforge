import json

from pyforge.config import load_settings, save_settings
from pyforge.models import Settings


def test_corrupted_settings_fall_back_to_defaults(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("{broken", encoding="utf-8")
    assert load_settings(path) == Settings()


def test_settings_round_trip(tmp_path):
    path = tmp_path / "settings.json"
    settings = Settings(theme="light", history_enabled=False)
    save_settings(settings, path)
    assert json.loads(path.read_text())["theme"] == "light"
    assert load_settings(path) == settings
