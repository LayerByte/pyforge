def test_base64_encode_handles_unicode():
    from pyforge.tools.encoding.core import base64_encode

    assert base64_encode("žluť") == "xb5sdcWl"


def test_base64_decode_rejects_malformed_input():
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.encoding.core import base64_decode

    assert base64_decode("aGVsbG8=") == "hello"
    with pytest.raises(ValidationError):
        base64_decode("@@")


def test_url_encode_escapes_reserved_characters():
    from pyforge.tools.encoding.core import url_encode

    assert url_encode("a b/c") == "a%20b%2Fc"


def test_url_decode_restores_unicode():
    from pyforge.tools.encoding.core import url_decode

    assert url_decode("%C5%BElu%C5%A5") == "žluť"


def test_hex_encode_uses_utf8_bytes():
    from pyforge.tools.encoding.core import hex_encode

    assert hex_encode("Až") == "41c5be"


def test_hex_decode_rejects_invalid_data():
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.encoding.core import hex_decode

    assert hex_decode("6869") == "hi"
    with pytest.raises(ValidationError):
        hex_decode("xyz")


def test_html_escape_handles_quotes_and_tags():
    from pyforge.tools.encoding.core import html_escape

    assert html_escape('<a title="x">') == "&lt;a title=&quot;x&quot;&gt;"


def test_html_unescape_resolves_named_entities():
    from pyforge.tools.encoding.core import html_unescape

    assert html_unescape("Tom &amp; Jerry") == "Tom & Jerry"
