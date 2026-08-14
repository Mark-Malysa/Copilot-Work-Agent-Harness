from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from cwah.agent.loop import process_response
from cwah.agent.session import SessionStore
from cwah.config import Config
from cwah.context.builder import build_context
from cwah.context.explicit_refs import find_explicit_refs
from cwah.context.files import workspace_files
from cwah.context.search import search
from cwah.graph.graphify import GraphifyAdapter, GraphResult
from cwah.protocol.parser import ProtocolError, parse_response, repair_prompt
from cwah.security.paths import PathSecurityError, Workspace
from cwah.security.secrets import is_filtered
from cwah.tools.edit_file import EditError, apply_search_replace, create_file
from cwah.tools.run_command import UnsafeCommand, run_command, validate_command
from cwah.transport.clipboard import MemoryClipboard
from cwah.workspace import resolve_workspace


def resp(json: str, payload: str = "") -> str:
    return f"prose\nCWAH_RESPONSE_V1_START\n{json}\n{payload}\nCWAH_RESPONSE_V1_END\nmore"


def gitrepo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    return tmp_path


@pytest.mark.parametrize("path", ["../x", "../../etc/passwd"])
def test_traversal(tmp_path: Path, path: str):
    with pytest.raises(PathSecurityError):
        Workspace(tmp_path).resolve(path)


def test_absolute_outside(tmp_path: Path):
    with pytest.raises(PathSecurityError):
        Workspace(tmp_path).resolve(tmp_path.parent / "x")


def test_scope_and_context(tmp_path: Path):
    w = Workspace(tmp_path, "src", ["docs"])
    assert (
        w.in_read_scope("docs/a.md")
        and not w.in_write_scope("docs/a.md")
        and w.in_write_scope("src/a.py")
    )
    assert Workspace(tmp_path, r"src\nested").scope == (tmp_path / "src/nested").resolve()


def test_nested_workspace_does_not_expose_git_siblings(tmp_path: Path):
    gitrepo(tmp_path)
    workspace = tmp_path / "monday_bde"
    for name in ["docs/design.md", "src/pipeline.py", "tests/test_pipeline.py"]:
        path = workspace / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(name, "utf-8")
    for name in ["unrelated_one/random.py", "unrelated_two/random2.py"]:
        path = tmp_path / name
        path.parent.mkdir(parents=True)
        path.write_text(name, "utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)

    info = resolve_workspace(Path("."), r"src\pipeline", invocation=workspace)
    tracked, untracked = workspace_files(workspace)
    visible = tracked + untracked
    assert info.root == workspace.resolve()
    assert info.git and info.git.root == tmp_path.resolve()
    assert info.scope == "src/pipeline"
    assert set(visible) == {"docs/design.md", "src/pipeline.py", "tests/test_pipeline.py"}
    assert not any("unrelated" in name for name in visible)


def test_linked_worktree_git_file_and_common_dir(tmp_path: Path):
    main = tmp_path / "main"
    linked = tmp_path / "linked"
    main.mkdir()
    gitrepo(main)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=main, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=main, check=True)
    (main / "tracked.txt").write_text("main", "utf-8")
    subprocess.run(["git", "add", "."], cwd=main, check=True)
    subprocess.run(["git", "commit", "-qm", "initial"], cwd=main, check=True)
    subprocess.run(
        ["git", "worktree", "add", "-qb", "linked-test", str(linked)], cwd=main, check=True
    )

    info = resolve_workspace(linked, invocation=tmp_path)
    assert (linked / ".git").is_file()
    assert info.git and info.git.root == linked.resolve()
    assert info.git.common_dir == (main / ".git").resolve()
    assert info.git.branch == "linked-test"


def test_symlink_escape(tmp_path: Path):
    outside = tmp_path.parent / "outside"
    outside.mkdir(exist_ok=True)
    link = tmp_path / "link"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlink unavailable")
    with pytest.raises(PathSecurityError):
        Workspace(tmp_path).resolve("link/a")


def test_protocol_variants():
    j = '{"status":"continue","actions":[{"id":"a","type":"git_status"}]}'
    assert parse_response(resp(j)).control.actions[0].type == "git_status"
    assert (
        parse_response(
            f"CWAH_RESPONSE_V1_START\n```json\n{j}\n```\nCWAH_RESPONSE_V1_END"
        ).control.status
        == "continue"
    )


def test_payloads():
    j = '{"status":"continue","actions":[{"id":"a","type":"create_file","path":"a","payload_id":"one"},{"id":"b","type":"create_file","path":"b","payload_id":"two"}]}'
    p = "CWAH_PAYLOAD_START one\na\nCWAH_PAYLOAD_END one\nCWAH_PAYLOAD_START two\nb\nCWAH_PAYLOAD_END two"
    assert parse_response(resp(j, p)).payloads == {"one": "a", "two": "b"}


@pytest.mark.parametrize(
    "text",
    [
        "x",
        "CWAH_RESPONSE_V1_START\nnope\nCWAH_RESPONSE_V1_END",
        resp('{"status":"continue","actions":[{"id":"a","type":"unknown"}]}'),
        resp('{"status":"continue","actions":[{"id":"a","type":"read_file"}]}'),
    ],
)
def test_bad_protocol(text: str):
    with pytest.raises(ProtocolError):
        parse_response(text)


def test_repair():
    assert "SAME intended actions" in repair_prompt(ValueError("bad"))


def test_edits(tmp_path: Path):
    p = tmp_path / "a"
    p.write_text("one\ntwo\nthree\n", "utf-8")
    payload = "<<<<<<< SEARCH\none\n=======\n1\n>>>>>>> REPLACE\n<<<<<<< SEARCH\nthree\n=======\n3\n>>>>>>> REPLACE"
    assert apply_search_replace(p, payload) == 2
    assert p.read_text() == "1\ntwo\n3\n"


def test_edit_missing_ambiguous(tmp_path: Path):
    p = tmp_path / "a"
    p.write_text("x x", "utf-8")
    with pytest.raises(EditError, match="ambiguous"):
        apply_search_replace(p, "<<<<<<< SEARCH\nx\n=======\ny\n>>>>>>> REPLACE")
    with pytest.raises(EditError, match="not found"):
        apply_search_replace(p, "<<<<<<< SEARCH\nz\n=======\ny\n>>>>>>> REPLACE")


def test_create(tmp_path: Path):
    p = tmp_path / "a/b"
    create_file(p, "yes")
    assert p.read_text() == "yes"
    with pytest.raises(EditError):
        create_file(p, "no")


def test_refs_context_filter_budget(tmp_path: Path):
    gitrepo(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/a.md").write_text("design")
    (tmp_path / "code.py").write_text("x=" + "x" * 20000)
    (tmp_path / ".env").write_text("SECRET=x")
    assert find_explicit_refs("Based on `docs/a.md`, work", tmp_path) == ["docs/a.md"]
    ctx = build_context(tmp_path, "Use docs/a.md", Config(context_budget_chars=6000))
    assert "design" in ctx.text and "SECRET" not in ctx.text and len(ctx.text) < 6000
    assert is_filtered("foo/.env") and is_filtered("x/private.zz", ["*.zz"])


def test_git_discovery_and_search(tmp_path: Path):
    gitrepo(tmp_path)
    (tmp_path / "a.py").write_text("needle here")
    subprocess.run(["git", "add", "a.py"], cwd=tmp_path, check=True)
    assert search(tmp_path, "needle")


def test_command(tmp_path: Path):
    r = run_command(
        f"\"{sys.executable}\" -c \"import sys;print('out');print('err',file=sys.stderr);sys.exit(3)\"",
        tmp_path,
    )
    assert r.exit_code == 3 and "out" in r.stdout and "err" in r.stderr and r.cwd == str(tmp_path)


def test_timeout(tmp_path: Path):
    assert run_command(f'"{sys.executable}" -c "import time;time.sleep(2)"', tmp_path, 1).timed_out


@pytest.mark.parametrize(
    "cmd", ["rm -rf /", "shutdown -h now", "format C:", "Remove-Item C:\\ -Recurse -Force"]
)
def test_destructive(cmd: str):
    with pytest.raises(UnsafeCommand):
        validate_command(cmd)


def test_session(tmp_path: Path):
    store = SessionStore(tmp_path)
    s = store.create(task="x", repo_root=str(tmp_path))
    s.iteration = 2
    s.completed = True
    store.save(s)
    loaded = store.load(s.id)
    assert loaded.iteration == 2 and loaded.completed and store.latest().id == s.id


def test_graph_unavailable(monkeypatch, tmp_path: Path):
    monkeypatch.setattr("shutil.which", lambda _: None)
    assert GraphifyAdapter(tmp_path).version() is None


def test_graph_mock(monkeypatch, tmp_path: Path):
    g = GraphifyAdapter(tmp_path)
    monkeypatch.setattr(g, "_run", lambda args: GraphResult(True, "file.py"))
    assert g.query("thing").ok and g.index().output == "file.py"


def test_loop_edit_and_complete(tmp_path: Path):
    gitrepo(tmp_path)
    (tmp_path / "a.py").write_text("bad\n")
    store = SessionStore(tmp_path)
    s = store.create(task="fix", repo_root=str(tmp_path))
    clip = MemoryClipboard()
    cfg = Config()
    edit = resp(
        '{"status":"continue","summary":"fix","actions":[{"id":"1","type":"edit_file","path":"a.py","payload_id":"p"}]}',
        "CWAH_PAYLOAD_START p\n<<<<<<< SEARCH\nbad\n=======\ngood\n>>>>>>> REPLACE\nCWAH_PAYLOAD_END p",
    )
    assert not process_response(edit, s, store, cfg, clip)
    assert (tmp_path / "a.py").read_text() == "good\n"
    assert "TOOL_RESULTS" in clip.value
    assert process_response(
        resp('{"status":"complete","summary":"done","actions":[]}'), s, store, cfg, clip
    )
    assert store.load(s.id).completed


def test_loop_repair(tmp_path: Path):
    s = SessionStore(tmp_path).create(task="x", repo_root=str(tmp_path))
    c = MemoryClipboard()
    assert not process_response("bad", s, SessionStore(tmp_path), Config(), c)
    assert "could not be parsed" in c.value
