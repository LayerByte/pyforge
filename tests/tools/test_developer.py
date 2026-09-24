def test_uuid_generator_returns_unique_valid_values():
    import uuid
    from pyforge.tools.developer.core import generate_uuids

    values = generate_uuids(5)
    assert len(set(values)) == 5 and all(uuid.UUID(value).version == 4 for value in values)


def test_timestamp_converter_normalizes_offsets():
    from pyforge.tools.developer.core import convert_timestamp

    result = convert_timestamp("1970-01-01T01:00:00+01:00")
    assert result["unix"] == 0 and result["utc"].endswith("+00:00")


def test_unix_time_converts_epoch():
    from pyforge.tools.developer.core import unix_time

    assert unix_time(0)["utc"].startswith("1970-01-01T00:00:00")


def test_random_string_honors_length_and_alphabet():
    from pyforge.tools.developer.core import random_string

    value = random_string(64, False)
    assert len(value) == 64 and value.isalnum()


def test_developer_json_tool_delegates_validation():
    from pyforge.tools.developer.core import developer_json_format

    assert developer_json_format('{"a":1}').startswith("{")


def test_developer_regex_tool_returns_matches():
    from pyforge.tools.developer.core import developer_regex_test

    assert developer_regex_test(r"\d+", "v12")[0]["value"] == "12"


def test_color_converter_round_trips_forms():
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.developer.core import convert_color

    assert (
        convert_color("#ff0080") == {"hex": "#FF0080", "rgb": (255, 0, 128)}
        and convert_color("255,0,128")["hex"] == "#FF0080"
    )
    with pytest.raises(ValidationError):
        convert_color("999,0,0")


def test_developer_url_parser_reuses_safe_parser():
    from pyforge.tools.developer.core import developer_url_parser

    assert developer_url_parser("https://example.test/api")["path"] == "/api"


def test_cron_explainer_handles_presets_and_invalid_input():
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.developer.core import explain_cron

    assert explain_cron("0 * * * *") == "At minute 0 of every hour"
    with pytest.raises(ValidationError):
        explain_cron("bad cron")


def test_environment_viewer_filters_and_redacts(monkeypatch):
    from pyforge.tools.developer.core import environment_variables

    monkeypatch.setenv("FORGE_VISIBLE", "yes")
    monkeypatch.setenv("FORGE_SECRET", "hidden")
    assert environment_variables("FORGE_") == {"FORGE_SECRET": "[REDACTED]", "FORGE_VISIBLE": "yes"}


def test_project_structure_shows_files(tmp_path):
    from pyforge.tools.developer.core import project_structure

    (tmp_path / "main.py").touch()
    assert any("main.py" in line for line in project_structure(tmp_path))


def test_source_line_count_classifies_python_lines(tmp_path):
    from pyforge.tools.developer.core import source_line_count

    (tmp_path / "a.py").write_text("# note\n\nx=1\n", encoding="utf-8")
    result = source_line_count(tmp_path)
    assert result == {"files": 1, "code": 1, "comments": 1, "blank": 1}
