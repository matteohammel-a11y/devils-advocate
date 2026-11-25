"""Cross-session memory: every saved debate is appended to memory.md (human-readable)
and memory.json (machine-readable, used for the History page)."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "memory.md"
JS = ROOT / "memory.json"


def load_history() -> list[dict]:
    try:
        return json.loads(JS.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def remember(entry: dict) -> None:
    entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), **entry}
    history = load_history() + [entry]
    JS.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    if not MD.exists():
        MD.write_text("# Memory: beliefs I have stress-tested\n", encoding="utf-8")
    with MD.open("a", encoding="utf-8") as f:
        f.write(f"\n## {entry['date']}: {entry['belief']}\n"
                f"- Confidence: {entry['before']} → {entry['after']}\n"
                f"- Take-away question: {entry.get('takeaway', '')}\n"
                f"- What would change my mind: {entry.get('change_mind', '') or '-'}\n")


def clear() -> None:
    for p in (MD, JS):
        p.unlink(missing_ok=True)
