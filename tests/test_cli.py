from typer.testing import CliRunner

from cwah.cli import app

runner = CliRunner()


def test_help():
    assert runner.invoke(app, ["--help"]).exit_code == 0


def test_doctor(tmp_path):
    result = runner.invoke(app, ["doctor", str(tmp_path)])
    assert result.exit_code == 0 and "Graphify" in result.stdout


def test_start_no_wait(tmp_path, monkeypatch):
    from cwah.transport.clipboard import SystemClipboard

    monkeypatch.setattr(SystemClipboard, "copy", lambda self, text: None)
    result = runner.invoke(app, ["start", str(tmp_path), "--task", "inspect", "--no-wait"])
    assert result.exit_code == 0 and "Initial prompt copied" in result.stdout
