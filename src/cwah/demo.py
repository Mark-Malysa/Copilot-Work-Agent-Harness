from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from cwah.agent.loop import run_scripted
from cwah.agent.session import SessionStore
from cwah.config import Config, TestingConfig
from cwah.transport.clipboard import MemoryClipboard


def response(control: str, payload: str = "") -> str:
    return f"CWAH_RESPONSE_V1_START\n{control}\n{payload}\nCWAH_RESPONSE_V1_END"


def run_demo(base: Path | None = None) -> tuple[bool, Path]:
    root = base or Path(tempfile.mkdtemp(prefix="cwah-demo-"))
    (root / "tests").mkdir(parents=True, exist_ok=True)
    (root / "calculator.py").write_text("def add(a, b):\n    return a - b\n", "utf-8")
    (root / "tests/test_calculator.py").write_text(
        "from calculator import add\n\ndef test_add():\n    assert add(2, 3) == 5\n", "utf-8"
    )
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    store = SessionStore(root)
    s = store.create(task="Fix add", repo_root=str(root), scope=".")
    responses = [
        response(
            '{"status":"continue","summary":"inspect","actions":[{"id":"1","type":"read_file","path":"calculator.py"}]}'
        ),
        response(
            '{"status":"continue","summary":"edit","actions":[{"id":"2","type":"edit_file","path":"calculator.py","payload_id":"p"}]}',
            "CWAH_PAYLOAD_START p\n<<<<<<< SEARCH\n    return a - b\n=======\n    return a + b\n>>>>>>> REPLACE\nCWAH_PAYLOAD_END p",
        ),
        response(
            '{"status":"continue","summary":"test","actions":[{"id":"3","type":"run_tests"}]}'
        ),
        response(
            '{"status":"complete","summary":"fixed","actions":[{"id":"4","type":"complete"}]}'
        ),
    ]
    return run_scripted(
        s,
        store,
        Config(testing=TestingConfig(command=f'"{__import__("sys").executable}" -m pytest')),
        MemoryClipboard(),
        responses,
    ), root
