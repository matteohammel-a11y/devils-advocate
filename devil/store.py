"""Shared storage for every debate, so many users build up one dataset.

- With SUPABASE_URL + SUPABASE_KEY set: stores in a Supabase (Postgres) table `debates`
  (see supabase_schema.sql). Works on Streamlit Cloud.
- Without them: falls back to a local file `debates.json` (fine on your own laptop).

The data powers three things: the Community page, the 👍/👎 feedback loop, and
"learning from the best": top-rated past Devil cases are shown to the Devil as examples.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx

LOCAL = Path(__file__).resolve().parent.parent / "debates.json"


def _cfg():
    return os.getenv("SUPABASE_URL", "").rstrip("/"), os.getenv("SUPABASE_KEY", "")


def backend() -> str:
    url, key = _cfg()
    return "supabase" if url and key else "local"


def _headers(key: str) -> dict:
    return {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json",
            "Prefer": "return=minimal"}


# ---- local fallback -------------------------------------------------------------------------
def _read_local() -> list[dict]:
    try:
        return json.loads(LOCAL.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _write_local(rows: list[dict]) -> None:
    LOCAL.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")


# ---- API ----------------------------------------------------------------------------------
def save(row: dict) -> str:
    """Insert a new debate; returns its id."""
    row = {"id": str(uuid.uuid4()), "created_at": datetime.now(timezone.utc).isoformat(), **row}
    url, key = _cfg()
    if url and key:
        r = httpx.post(f"{url}/rest/v1/debates", headers=_headers(key), json=row, timeout=20)
        r.raise_for_status()
    else:
        _write_local(_read_local() + [row])
    return row["id"]


def update(debate_id: str, fields: dict) -> None:
    url, key = _cfg()
    if url and key:
        r = httpx.patch(f"{url}/rest/v1/debates?id=eq.{debate_id}", headers=_headers(key),
                        json=fields, timeout=20)
        r.raise_for_status()
    else:
        rows = _read_local()
        for row in rows:
            if row["id"] == debate_id:
                row.update(fields)
        _write_local(rows)


def recent(limit: int = 200) -> list[dict]:
    url, key = _cfg()
    if url and key:
        r = httpx.get(f"{url}/rest/v1/debates?select=*&order=created_at.desc&limit={limit}",
                      headers=_headers(key), timeout=20)
        r.raise_for_status()
        return r.json()
    return sorted(_read_local(), key=lambda x: x.get("created_at", ""), reverse=True)[:limit]


def best_examples(exclude_restatement: str = "", k: int = 2) -> list[dict]:
    """Top-rated past Devil cases (👍, with a steelman) to show the Devil as examples."""
    try:
        rows = [r for r in recent(300) if r.get("rating") == 1 and r.get("steelman")
                and r.get("restatement") != exclude_restatement]
    except Exception:  # noqa: BLE001 (storage problems must never break a debate)
        return []
    rows.sort(key=lambda r: (len(r.get("feedback") or "") > 0, r.get("created_at", "")), reverse=True)
    return rows[:k]
