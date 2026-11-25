"""The Devil's Advocate pipeline (Version 4): Understand → Advocate ‖ Devil → Rebuttal →
blinded Judge → Reassess, plus a pushback turn governed by the concession rule.

Every stage is a separate model call with its own prompt file in prompts/.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYSTEM = (ROOT / "system.md").read_text(encoding="utf-8")


def load(name: str, folder: str = "prompts", **values) -> str:
    text = (ROOT / folder / f"{name}.md").read_text(encoding="utf-8")
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", str(val))
    return text


def as_text(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1)


@dataclass
class Debate:
    belief: str
    confidence: int
    language: str = "English"
    understanding: dict = field(default_factory=dict)
    restatement: str = ""
    advocate: dict = field(default_factory=dict)
    challenge: dict = field(default_factory=dict)
    oppose: dict = field(default_factory=dict)
    questions: list[str] = field(default_factory=list)
    rebuttals: dict = field(default_factory=dict)
    judge: dict = field(default_factory=dict)
    answers: list[str] = field(default_factory=list)
    reassess: dict = field(default_factory=dict)
    pushback: list[dict] = field(default_factory=list)  # chat turns
    skills_used: list[str] = field(default_factory=list)
    sources: list[dict] = field(default_factory=list)  # web evidence [1], [2], …
    search_error: str = ""
    examples: list[dict] = field(default_factory=list)  # top-rated past debates (learning loop)
    db_id: str = ""

    def evidence(self) -> str:
        """Numbered web sources for the prompts; empty when web search is off."""
        if not self.sources:
            return ""
        lines = ["\nWEB SOURCES. For factual claims, rely on these and cite them inline as [1], [2]. "
                 "Never cite a number that is not listed. If a claim is not backed by a source, "
                 "label it contested or unsupported. Sources can be wrong or one-sided: say so when relevant."]
        for s in self.sources:
            lines.append(f"[{s['n']}] {s['title']} ({s['url']})\n{s['content']}")
        return "\n".join(lines)

    def skills(self) -> str:
        """Skills are loaded only when Stage 1 says they are needed."""
        u, parts, self.skills_used = self.understanding, [], []
        if u.get("false_premise", {}).get("flag"):
            parts.append(load("false_premise", "skills", note=u["false_premise"].get("note", "")))
            self.skills_used.append("false_premise")
        if u.get("near_consensus", {}).get("flag"):
            parts.append(load("near_consensus", "skills", note=u["near_consensus"].get("note", "")))
            self.skills_used.append("near_consensus")
        if u.get("claim_type") == "personal_decision":
            parts.append(load("personal_decision", "skills"))
            self.skills_used.append("personal_decision")
        return ("\nExtra guidance:\n" + "\n\n".join(parts)) if parts else ""

    def examples_text(self) -> str:
        """Top-rated past challenges from other users, shown as examples of the quality bar."""
        if not self.examples:
            return ""
        parts = ["\nEXAMPLES of challenges that past users rated as genuinely useful (on OTHER beliefs). "
                 "Match their quality and specificity. Do not copy their content:"]
        for ex in self.examples:
            parts.append(f"- Belief: {ex.get('restatement', '')}\n  Strong opposing case: "
                         f"{(ex.get('steelman') or '')[:600]}")
        return "\n".join(parts)

    def devil_case(self) -> dict:
        return {"assumptions": self.challenge.get("assumptions", []),
                "claims": self.challenge.get("claims", []),
                "steelman": self.oppose.get("steelman", ""),
                "key_points": self.oppose.get("key_points", [])}


# ---- stages -------------------------------------------------------------------------

def understand(llm, d: Debate) -> None:
    d.understanding = llm.json(SYSTEM, load("understand", belief=d.belief, language=d.language))
    d.restatement = d.understanding.get("restatement", d.belief)


def research(d: Debate, api_key: str) -> None:
    """Web search (Tavily) with the neutral queries written in Stage 1."""
    from .search import gather
    queries = [q for q in d.understanding.get("search_queries", []) if isinstance(q, str) and q.strip()]
    d.sources = gather(queries or [d.restatement], api_key)


def advocate(llm, d: Debate) -> None:
    d.advocate = llm.json(SYSTEM, load("advocate", restatement=d.restatement, belief=d.belief,
                                       skills=d.skills(), evidence=d.evidence(), language=d.language))


def devil(llm, d: Debate, fast: bool = False) -> None:
    sk = d.skills()
    if fast:  # Stages 2–4 in one structured call: ~3x fewer calls
        out = llm.json(SYSTEM, load("devil_fast", restatement=d.restatement, belief=d.belief, skills=sk,
                                    evidence=d.evidence(), examples=d.examples_text(), language=d.language))
        d.challenge = {"assumptions": out.get("assumptions", []), "claims": out.get("claims", [])}
        d.oppose = {"steelman": out.get("steelman", ""), "key_points": out.get("key_points", [])}
        d.questions = [s for s in out.get("questions", []) if isinstance(s, str)][:3]
        return
    d.challenge = llm.json(SYSTEM, load("challenge", restatement=d.restatement, belief=d.belief,
                                        skills=sk, evidence=d.evidence(), language=d.language))
    assumptions = as_text(d.challenge.get("assumptions", []))
    d.oppose = llm.json(SYSTEM, load("oppose", restatement=d.restatement,
                                     assumptions=assumptions, skills=sk, evidence=d.evidence(),
                                     examples=d.examples_text(), language=d.language))
    q = llm.json(SYSTEM, load("question", restatement=d.restatement, assumptions=assumptions,
                              steelman=d.oppose.get("steelman", ""), language=d.language))
    d.questions = [s for s in q.get("questions", []) if isinstance(s, str)][:3]


def rebuttal(llm, d: Debate) -> None:
    """Both rebuttals run at the same time."""
    from concurrent.futures import ThreadPoolExecutor
    adv, dev = as_text(d.advocate), as_text(d.devil_case())
    with ThreadPoolExecutor(max_workers=2) as pool:
        fa = pool.submit(llm.json, SYSTEM, load("rebuttal", role="Advocate", restatement=d.restatement,
                                                own_case=adv, other_case=dev, language=d.language))
        fd = pool.submit(llm.json, SYSTEM, load("rebuttal", role="Devil", restatement=d.restatement,
                                                own_case=dev, other_case=adv, language=d.language))
        d.rebuttals = {"advocate": fa.result(), "devil": fd.result()}


def judge(llm, d: Debate) -> None:
    # Blinded: the Judge gets the neutral restatement only, never d.belief or d.confidence.
    d.judge = llm.json(SYSTEM, load("judge", restatement=d.restatement,
                                    advocate=as_text(d.advocate), devil=as_text(d.devil_case()),
                                    rebuttals=as_text(d.rebuttals), evidence=d.evidence(),
                                    language=d.language))


def reassess(llm, d: Debate) -> None:
    qa = "\n".join(f"Q{i+1}: {q}\nA{i+1}: {a or '(no answer)'}"
                   for i, (q, a) in enumerate(zip(d.questions, d.answers)))
    d.reassess = llm.json(SYSTEM, load("reassess", restatement=d.restatement,
                                       confidence=d.confidence, answers=qa,
                                       judge=as_text(d.judge), language=d.language))


def push_back(llm, d: Debate, message: str) -> dict:
    history = [{"role": t["role"], "content": t["content"]} for t in d.pushback]
    reply = llm.json(SYSTEM + "\n\n" + load("pushback", restatement=d.restatement,
                                            steelman=d.oppose.get("steelman", ""),
                                            language=d.language),
                     message, history=history)
    d.pushback.append({"role": "user", "content": message})
    d.pushback.append({"role": "assistant", "content": reply.get("reply", ""), "meta": reply})
    return reply
