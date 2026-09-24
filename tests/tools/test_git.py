def test_repository_information_combines_safe_git_queries(monkeypatch):
    import pyforge.tools.git.core as module

    values = {"--show-toplevel": "/repo", "--show-current": "main", "-v": "origin x", "--porcelain": ""}
    monkeypatch.setattr(module, "_git", lambda repo, *args: values[args[-1]])
    assert module.repository_information()["clean"] and module.repository_information()["branch"] == "main"


def test_current_branch_handles_detached_head(monkeypatch):
    import pyforge.tools.git.core as module

    monkeypatch.setattr(module, "_git", lambda *args: "")
    assert module.current_branch() == "[detached HEAD]"


def test_branch_list_marks_current_branch(monkeypatch):
    import pyforge.tools.git.core as module

    monkeypatch.setattr(module, "_git", lambda *args: "*\tmain\n \tdev")
    assert module.branch_list()[0] == {"name": "main", "current": True}


def test_commit_history_parses_fields(monkeypatch):
    import pyforge.tools.git.core as module

    monkeypatch.setattr(module, "_git", lambda *args: "abc	2026-01-01T00:00:00Z	Ada	feat: add tool")
    assert module.commit_history()[0]["subject"] == "feat: add tool"


def test_contributor_summary_orders_by_commit_count(monkeypatch):
    import pyforge.tools.git.core as module

    monkeypatch.setattr(module, "_git", lambda *args: "Ada <a@x>\nBob <b@x>\nAda <a@x>")
    assert module.contributor_summary()[0]["commits"] == 2


def test_repository_statistics_counts_extensions(monkeypatch):
    import pyforge.tools.git.core as module

    monkeypatch.setattr(module, "_git", lambda repo, *args: "a.py\nb.py\nREADME" if args[0] == "ls-files" else "4")
    result = module.repository_statistics()
    assert result["tracked_files"] == 3 and result["extensions"][".py"] == 2


def test_changed_files_parses_porcelain_status(monkeypatch):
    import pyforge.tools.git.core as module

    monkeypatch.setattr(module, "_git", lambda *args: " M README.md\nA  new.py")
    assert module.changed_files()[1]["index"] == "A"


def test_untracked_files_returns_git_output(monkeypatch):
    import pyforge.tools.git.core as module

    monkeypatch.setattr(module, "_git", lambda *args: "a.tmp\nnotes.txt")
    assert module.untracked_files() == ["a.tmp", "notes.txt"]


def test_gitignore_checker_reports_subprocess_result(monkeypatch):
    from types import SimpleNamespace
    import pyforge.tools.git.core as module

    monkeypatch.setattr(
        "subprocess.run", lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout=".gitignore:1:*.tmp a.tmp\n")
    )
    assert module.gitignore_check(".", ["a.tmp"])[0]["ignored"]


def test_large_tracked_files_uses_repository_root(tmp_path, monkeypatch):
    import pyforge.tools.git.core as module

    (tmp_path / "large.bin").write_bytes(b"12345")
    monkeypatch.setattr(module, "_git", lambda repo, *args: str(tmp_path) if args[0] == "rev-parse" else "large.bin")
    assert module.large_tracked_files(tmp_path, 5)[0]["size"] == 5
