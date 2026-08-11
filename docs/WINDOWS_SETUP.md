# Windows setup

## Requirements and install (PowerShell)

Install 64-bit Python 3.11+ and Git for Windows, then reopen PowerShell. Optional uv installation:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# reopen PowerShell if uv is not yet on PATH
git clone https://github.com/Mark-Malysa/Copilot-Work-Agent-Harness.git
cd Copilot-Work-Agent-Harness
uv sync --extra dev
uv run cwah doctor
uv run cwah demo
```

Without uv: `py -3.11 -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install .`. Transfer the repository by Git or an approved archive and repeat installation—do not copy a virtual environment between machines.

## Use

```powershell
cd C:\work\project
C:\path\to\Copilot-Work-Agent-Harness\.venv\Scripts\cwah.exe start . --scope src\area
```

Add that `Scripts` directory to user PATH, or use `uv run --project C:\path\to\CWAH cwah ...`. `where.exe python`, `where.exe git`, and `where.exe cwah` diagnose PATH issues. Clipboard errors can result from headless/RDP sessions or policy; use `cwah ingest-response response.txt`. Configure Git identity only if you personally commit (`git config --global user.name ...`).

Graphify is optional: install its CLI using its upstream instructions, ensure `graphify --version` works, and use only its local/code-only mode. CWAH continues without it.

## Standalone executable

On Windows, `uv run python scripts/build_exe.py` (dev extra required) produces `dist\cwah.exe`. Copy it to an approved location and run `dist\cwah.exe doctor`. Graphify remains a separate optional executable. This build is not cross-compiled or signed.

Corporate application-control, endpoint-security, repository, and data-handling policy may prohibit personal executables or sharing source with Copilot. CWAH does not bypass those controls; ask your organization.
