from pathlib import Path

from cwah.demo import run_demo


def test_demo(tmp_path: Path):
    ok, root = run_demo(tmp_path)
    assert ok
    assert "a + b" in (root / "calculator.py").read_text()
    assert (root / ".cwah/sessions").exists()
