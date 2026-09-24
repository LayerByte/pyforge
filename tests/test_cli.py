from typer.testing import CliRunner

from pyforge.cli import app

runner = CliRunner()


def test_version_command_reports_package_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0 and "PyForge 1.0.0" in result.stdout


def test_version_option_reports_package_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0 and "PyForge 1.0.0" in result.stdout


def test_help_lists_primary_workflows():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "interactive" in result.stdout and "run" in result.stdout and "export" in result.stdout


def test_describe_command_reports_tool_metadata():
    result = runner.invoke(app, ["describe", "text.slugify"])
    assert result.exit_code == 0
    assert "Slug Generator" in result.stdout and "text.slugify" in result.stdout


def test_search_command_finds_tools_by_description():
    result = runner.invoke(app, ["search", "reading time"])
    assert result.exit_code == 0
    assert "text.statistics" in result.stdout


def test_run_command_rejects_non_object_arguments():
    result = runner.invoke(app, ["run", "text.word-count", "--arguments", "[]"])
    assert result.exit_code == 1
    assert "arguments must be a JSON object" in result.stdout


def test_tools_command_reports_unknown_category():
    result = runner.invoke(app, ["tools", "missing"])
    assert result.exit_code == 1
    assert "No tools found" in result.stdout
