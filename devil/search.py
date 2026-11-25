"""Web search tool (Tavily), as in class. Results become numbered sources [1], [2], … that the
Advocate, the Devil and the Judge must cite."""
from __future__ import annotations

import os

import httpx

TAVILY_URL = "https://api.tavily.com/search"
DEFAULT_KEY = os.getenv("TAVILY_API_KEY", "")


def tavily_search(query: str, api_key: str, max_results: int = 4) -> list[dict]:
    r = httpx.post(TAVILY_URL, timeout=30,
                   headers={"Authorization": f"Bearer {api_key}"},
                   json={"query": query, "max_results": max_results, "search_depth": "basic"})
    r.raise_for_status()
    return [{"title": x.get("title", ""), "url": x.get("url", ""),
             "content": (x.get("content") or "")[:600]} for x in r.json().get("results", [])]


def gather(queries: list[str], api_key: str, per_query: int = 4) -> list[dict]:
    """Run several queries and return de-duplicated sources, numbered from 1."""
    seen, sources = set(), []
    for q in queries[:3]:
        for res in tavily_search(q, api_key, per_query):
            if res["url"] and res["url"] not in seen:
                seen.add(res["url"])
                sources.append({**res, "n": len(sources) + 1, "query": q})
    return sources[:10]
