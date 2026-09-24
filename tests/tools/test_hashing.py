def test_text_hash_supports_sha512_and_rejects_unknown():
    import pytest
    from pyforge.errors import ValidationError
    from pyforge.tools.hashing.core import hash_text

    assert len(hash_text("hello", "sha512")) == 128
    with pytest.raises(ValidationError):
        hash_text("hello", "crc32")


def test_file_hash_streams_binary_input(tmp_path):
    from pyforge.tools.hashing.core import hash_file

    path = tmp_path / "binary"
    path.write_bytes(bytes(range(256)) * 100)
    assert len(hash_file(path, "sha384")) == 96


def test_hash_comparison_ignores_case_and_spacing():
    from pyforge.tools.hashing.core import compare_hashes

    assert compare_hashes("AA BB", "aabb") and not compare_hashes("aa", "ab")
