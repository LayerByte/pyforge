def test_json_formatter_preserves_unicode_and_validates():
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.json_tools.core import format_json

    assert '"ž"' in format_json('{"name":"ž"}')
    with pytest.raises(ValidationError):
        format_json("{")


def test_json_minifier_removes_whitespace():
    from pyforge.tools.json_tools.core import minify_json

    assert minify_json('{ "a": 1, "b": [2] }') == '{"a":1,"b":[2]}'


def test_json_validator_reports_location():
    from pyforge.tools.json_tools.core import validate_json

    assert validate_json("[]")["valid"]
    result = validate_json('{\n"a": }')
    assert not result["valid"] and result["error"]["line"] == 2


def test_json_view_flattens_nested_values():
    from pyforge.tools.json_tools.core import json_view

    assert json_view('{"a":[{"b":2}]}') == [{"path": "a[0].b", "value": 2}]


def test_json_statistics_counts_nested_types():
    from pyforge.tools.json_tools.core import json_statistics

    result = json_statistics('{"a":[1,true,null]}')
    assert result["objects"] == 1 and result["arrays"] == 1 and result["values"] == 3 and result["max_depth"] == 2


def test_json_key_search_reports_paths():
    from pyforge.tools.json_tools.core import search_json_keys

    assert search_json_keys('{"User":{"userId":3}}', "user")[1]["path"] == "User.userId"


def test_json_comparison_reports_changed_path():
    from pyforge.tools.json_tools.core import compare_json

    result = compare_json('{"a":1}', '{"a":2}')
    assert not result["equal"] and result["differences"][0]["path"] == "a"
