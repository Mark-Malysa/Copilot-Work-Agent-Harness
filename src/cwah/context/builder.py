from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cwah.config import Config
from cwah.context.explicit_refs import find_explicit_refs
from cwah.context.files import read_snippet, tracked_files
from cwah.security.secrets import is_filtered
from cwah.workspace import normalize_relative


@dataclass
class BuiltContext:
    text: str
    files: list[str]
    omitted: list[str]


def build_context(root: Path, task: str, config: Config) -> BuiltContext:
    files = tracked_files(root, config.exclude.patterns)
    refs = find_explicit_refs(task, root)
    scope = normalize_relative(config.scope)
    selected = (
        refs
        + [f for f in files if (scope == "." or f.startswith(scope + "/")) and f not in refs][:30]
    )
    tree = "\n".join(files[:250])
    sections = [
        f"TASK\n{task}",
        f"WORKSPACE {root}\nSCOPE {scope}\nFILES (first 250)\n{tree}",
    ]
    used = sum(map(len, sections))
    included = []
    omitted = []
    reserve = min(6000, config.context_budget_chars // 6)
    for name in selected:
        if is_filtered(name, config.exclude.patterns):
            omitted.append(name + " (filtered)")
            continue
        try:
            content, start, end, truncated = read_snippet(root / name, 8000)
        except OSError:
            continue
        block = f"FILE {name} lines {start}-{end}{' (snippet)' if truncated else ''}\n```\n{content}\n```"
        if used + len(block) > config.context_budget_chars - reserve:
            omitted.append(name)
            continue
        sections.append(block)
        used += len(block)
        included.append(name)
    if omitted:
        sections.append("OMITTED DUE TO FILTER/BUDGET: " + ", ".join(omitted))
    return BuiltContext("\n\n".join(sections), included, omitted)
