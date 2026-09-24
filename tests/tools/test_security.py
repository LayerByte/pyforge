def test_password_strength_rewards_length_and_variety():
    from pyforge.tools.security.core import password_strength

    assert password_strength("correct horse battery staple 42!")["score"] > password_strength("password")["score"]


def test_file_hash_checker_detects_expected_digest(tmp_path):
    from pyforge.tools.security.core import check_file_hash

    path = tmp_path / "x"
    path.write_text("abc")
    assert check_file_hash(path, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")["match"]


def test_file_entropy_handles_empty_and_uniform_files(tmp_path):
    from pyforge.tools.security.core import file_entropy

    empty = tmp_path / "empty"
    empty.touch()
    uniform = tmp_path / "uniform"
    uniform.write_bytes(b"A" * 20)
    assert file_entropy(empty)["entropy"] == 0 and file_entropy(uniform)["entropy"] == 0


def test_secret_detector_redacts_assignment_value():
    from pyforge.tools.security.core import detect_secrets

    text = "api_key=" + "sensitive" + "value"
    result = detect_secrets(text)
    assert result and "sensitivevalue" not in result[0]["preview"]


def test_permission_inspector_reports_mode(tmp_path):
    from pyforge.tools.security.core import inspect_permissions

    path = tmp_path / "x"
    path.write_text("x")
    result = inspect_permissions(path)
    assert result["owner_read"] and result["path"] == str(path)


def test_environment_secret_warning_never_returns_value(monkeypatch):
    from pyforge.tools.security.core import environment_secret_warnings

    monkeypatch.setenv("PYFORGE_API_KEY", "do-not-show")
    result = environment_secret_warnings()
    item = next(x for x in result if x["name"] == "PYFORGE_API_KEY")
    assert item["value"] == "[REDACTED]"


def test_security_header_analyzer_scores_present_headers():
    from pyforge.tools.security.core import analyze_security_headers

    result = analyze_security_headers(
        {"Content-Security-Policy": "default-src 'self'", "X-Content-Type-Options": "nosniff"}
    )
    assert result["score"] == 40 and len(result["missing"]) == 3


def test_tls_certificate_viewer_validates_before_network():
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.security.core import tls_certificate_information

    with pytest.raises(ValidationError):
        tls_certificate_information("bad host")
    with pytest.raises(ValidationError):
        tls_certificate_information("example.test", 0)
