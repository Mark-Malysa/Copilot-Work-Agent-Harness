from __future__ import annotations

import shutil
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from cwah.agent.loop import process_response
from cwah.agent.session import SessionStore
from cwah.config import load_config
from cwah.context.builder import build_context
from cwah.demo import run_demo
from cwah.graph.graphify import GraphifyAdapter
from cwah.protocol.prompts import initial_prompt
from cwah.tools.git_tools import git, snapshot
from cwah.transport.clipboard import ClipboardError, SystemClipboard

app = typer.Typer(
    help="Copilot Work Agent Harness — a safe manual clipboard coding agent.", no_args_is_help=True
)
console = Console()


def root(path: Path) -> Path:
    p = path.resolve()
    top = git(p, "rev-parse", "--show-toplevel")
    return Path(top).resolve() if top and "fatal:" not in top else p


def approval(message: str) -> bool:
    return typer.confirm(f"Copilot requests: {message}. Approve?", default=False)


@app.command()
def doctor(repo: Path = typer.Argument(Path("."))) -> None:
    r = root(repo)
    cfg = load_config(r)
    table = Table(title="CWAH Doctor")
    table.add_column("Check")
    table.add_column("Result")
    clip = SystemClipboard()
    checks = [
        ("Python", sys.version.split()[0]),
        ("Git", shutil.which("git") or "not found"),
        (
            "Repository",
            "valid"
            if (r / ".git").exists() or git(r, "rev-parse", "--is-inside-work-tree") == "true"
            else "not a Git repository",
        ),
        ("Clipboard", "available" if clip.available() else "unavailable (use ingest-response)"),
        ("Graphify", GraphifyAdapter(r).version() or "unavailable; fallback enabled"),
        ("ripgrep", shutil.which("rg") or "unavailable; Python fallback enabled"),
        ("Scope", cfg.scope),
        ("Directory", str(r)),
    ]
    for row in checks:
        table.add_row(*row)
    console.print(table)


@app.command()
def start(
    repo: Path = typer.Argument(Path(".")),
    scope: str | None = typer.Option(None, "--scope"),
    context: list[str] = typer.Option([], "--context"),
    task: str | None = typer.Option(None, "--task"),
    no_wait: bool = typer.Option(False, "--no-wait"),
) -> None:
    r = root(repo)
    cfg = load_config(r)
    cfg.scope = scope or cfg.scope
    cfg.context_dirs = context or cfg.context_dirs
    task = task or typer.prompt("Task")
    ctx = build_context(r, task, cfg)
    store = SessionStore(r)
    s = store.create(
        task=task,
        repo_root=str(r),
        scope=cfg.scope,
        context_dirs=cfg.context_dirs,
        relevant_files=ctx.files,
        initial_git=snapshot(r),
    )
    clip = SystemClipboard()
    prompt = initial_prompt(s, ctx.text)
    try:
        clip.copy(prompt)
    except ClipboardError as e:
        console.print(f"[red]Clipboard failed:[/] {e}\nPrompt saved to .cwah/prompt.txt")
        (r / ".cwah").mkdir(exist_ok=True)
        (r / ".cwah/prompt.txt").write_text(prompt, "utf-8")
        return
    console.print(
        f"[bold]Copilot Work Agent Harness[/]\nRepo: {r}\nScope: {cfg.scope}\nSession: {s.id}\n[green]Initial prompt copied.[/] Paste it into Copilot, copy the entire reply, return and press Enter."
    )
    if no_wait:
        return
    while not s.completed and s.iteration < cfg.iteration_limit:
        typer.prompt("Press ENTER after copying Copilot's reply", default="", show_default=False)
        if process_response(clip.paste(), s, store, cfg, clip, approval):
            console.print("[green]Task complete[/]")
            break
        console.print("Next prompt copied (or protocol repair prompt if parsing failed).")


@app.command("ingest-response")
def ingest_response(file: Path, repo: Path = Path(".")) -> None:
    r = root(repo)
    cfg = load_config(r)
    store = SessionStore(r)
    s = store.latest()
    clip = SystemClipboard()
    try:
        done = process_response(file.read_text("utf-8"), s, store, cfg, clip, approval)
    except ClipboardError:
        done = s.completed
    console.print("Task complete" if done else "Response processed; next prompt copied")


@app.command()
def sessions(repo: Path = Path(".")) -> None:
    for s in SessionStore(root(repo)).list():
        console.print(
            f"{s.id}  iteration={s.iteration}  {'complete' if s.completed else 'active'}  {s.task}"
        )


@app.command()
def resume(session_id: str, repo: Path = Path(".")) -> None:
    r = root(repo)
    s = SessionStore(r).load(session_id)
    console.print(
        f"Resume {s.id}: {s.task}\nRun `cwah context --full`, paste it into Copilot, then use `cwah ingest-response FILE` or `cwah start` interactive loop."
    )


@app.command()
def status(repo: Path = Path(".")) -> None:
    r = root(repo)
    s = SessionStore(r).latest()
    console.print(s.model_dump_json(indent=2, exclude={"actions", "command_results"}))


@app.command()
def changes(repo: Path = Path(".")) -> None:
    console.print(git(root(repo), "diff", "--no-ext-diff"))


@app.command("context")
def context_command(repo: Path = Path("."), full: bool = typer.Option(False, "--full")) -> None:
    r = root(repo)
    s = SessionStore(r).latest()
    ctx = build_context(r, s.task, load_config(r))
    text = initial_prompt(s, ctx.text) if full else ctx.text
    console.print(text)


@app.command()
def index(repo: Path = Path("."), scope: str | None = None) -> None:
    r = root(repo)
    cfg = load_config(r)
    g = GraphifyAdapter(r)
    if not cfg.graphify.enabled:
        console.print("Graphify disabled in .cwah.toml")
        raise typer.Exit()
    if not g.version():
        console.print("Graphify unavailable; CWAH will use Git/search fallback.")
        raise typer.Exit()
    result = g.index(scope or cfg.scope)
    console.print(result.output)
    raise typer.Exit(code=0 if result.ok else 1)


@app.command()
def demo() -> None:
    ok, path = run_demo()
    console.print(f"{'[green]Demo passed[/]' if ok else '[red]Demo failed[/]'}: {path}")
    raise typer.Exit(code=0 if ok else 1)


if __name__ == "__main__":
    app()
