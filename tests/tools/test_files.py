def test_file_information_reports_metadata(tmp_path):
    from pyforge.tools.files.core import file_information

    path = tmp_path / "sample.txt"
    path.write_text("hello", encoding="utf-8")
    result = file_information(path)
    assert result["size"] == 5 and result["suffix"] == ".txt" and result["is_file"]


def test_file_hash_matches_known_sha256(tmp_path):
    from pyforge.tools.files.core import file_hash

    path = tmp_path / "data"
    path.write_bytes(b"abc")
    assert file_hash(path) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_file_comparison_detects_changes(tmp_path):
    from pyforge.tools.files.core import compare_files

    a = tmp_path / "a"
    b = tmp_path / "b"
    a.write_text("same")
    b.write_text("same")
    assert compare_files(a, b)["same_content"]
    b.write_text("different")
    assert not compare_files(a, b)["same_content"]


def test_duplicate_finder_groups_equal_files(tmp_path):
    from pyforge.tools.files.core import find_duplicates

    (tmp_path / "a").write_text("copy")
    (tmp_path / "b").write_text("copy")
    (tmp_path / "c").write_text("other")
    assert len(find_duplicates(tmp_path)) == 1


def test_directory_statistics_counts_nested_entries(tmp_path):
    from pyforge.tools.files.core import directory_statistics

    (tmp_path / "sub").mkdir()
    (tmp_path / "a.py").write_text("x")
    (tmp_path / "sub" / "b.py").write_text("yy")
    result = directory_statistics(tmp_path)
    assert result["files"] == 2 and result["directories"] == 1 and result["bytes"] == 3


def test_directory_tree_respects_depth(tmp_path):
    from pyforge.tools.files.core import directory_tree

    (tmp_path / "one" / "two").mkdir(parents=True)
    (tmp_path / "one" / "two" / "x").write_text("x")
    text = "\n".join(directory_tree(tmp_path, max_depth=1))
    assert "one/" in text and "two/" not in text


def test_file_search_applies_pattern(tmp_path):
    from pyforge.tools.files.core import search_files

    (tmp_path / "a.py").write_text("")
    (tmp_path / "b.txt").write_text("")
    assert search_files(tmp_path, "*.py") == [str(tmp_path / "a.py")]


def test_large_file_finder_uses_inclusive_threshold(tmp_path):
    from pyforge.tools.files.core import find_large_files

    (tmp_path / "large").write_bytes(b"12345")
    (tmp_path / "small").write_bytes(b"1")
    assert [x["path"] for x in find_large_files(tmp_path, 5)] == [str(tmp_path / "large")]


def test_empty_file_finder_ignores_nonempty_files(tmp_path):
    from pyforge.tools.files.core import find_empty_files

    (tmp_path / "empty").touch()
    (tmp_path / "full").write_text("x")
    assert find_empty_files(tmp_path) == [str(tmp_path / "empty")]


def test_extension_statistics_normalizes_case(tmp_path):
    from pyforge.tools.files.core import extension_statistics

    (tmp_path / "a.PY").touch()
    (tmp_path / "b.py").touch()
    (tmp_path / "README").touch()
    assert extension_statistics(tmp_path) == {".py": 2, "[none]": 1}


def test_integrity_snapshot_uses_relative_paths(tmp_path):
    from pyforge.tools.files.core import integrity_snapshot

    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "a").write_text("x")
    snapshot = integrity_snapshot(tmp_path)
    assert list(snapshot) == ["sub/a"] and len(snapshot["sub/a"]) == 64
