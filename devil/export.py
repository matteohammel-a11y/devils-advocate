"""Export a full debate as Markdown (for the iteration log, the report or sharing)."""
from __future__ import annotations

from datetime import datetime

from .pipeline import Debate


def _list(xs) -> str:
    return "\n".join(f"- {x}" for x in xs or []) or "-"


def to_markdown(d: Debate, model: str, after: int | None = None, change_mind: str = "") -> str:
    adv, ch, op, j, r = d.advocate, d.challenge, d.oppose, d.judge, d.reassess
    out = [f"# Devil's Advocate: debate log",
           f"*{datetime.now():%Y-%m-%d %H:%M} · model `{model}` · language {d.language}*\n",
           f"**Belief:** {d.belief}  \n**Confidence before:** {d.confidence}/100"
           + (f"  \n**Confidence after:** {after}/100" if after is not None else ""),
           f"\n## 1 · Understand\n{d.restatement}\n\nType: `{d.understanding.get('claim_type','')}`"
           f" · skills loaded: {', '.join(d.skills_used) or 'none'}",
           f"\n## 2 · Advocate\n{adv.get('summary','')}\n"]
    out += [f"- **{a.get('claim','')}** ({a.get('evidence','')}): {a.get('reasoning','')}"
            for a in adv.get("arguments", [])]
    out.append(f"\n*Reasons not mentioned:*\n{_list(adv.get('unmentioned_reasons'))}")
    out.append("\n## 3 · Devil\n### Load-bearing assumptions")
    out += [f"- **{a.get('assumption','')}** ({a.get('evidence','')}): {a.get('why_load_bearing','')}"
            for a in ch.get("assumptions", [])]
    out.append("### Claims checked")
    out += [f"- {c.get('claim','')}: *{c.get('evidence','')}* ({c.get('note','')})"
            for c in ch.get("claims", [])]
    out.append(f"### Steelman\n> {op.get('steelman','')}")
    out.append("\n## 4 · Rebuttals")
    for side, rb in d.rebuttals.items():
        out.append(f"**{side.title()}:** {rb.get('rebuttal','')}  \n*Concedes:* "
                   f"{'; '.join(rb.get('concessions', []) or []) or '-'}")
    out.append(f"\n## 5 · Judge (blinded)\n**Survived:**\n{_list(j.get('survived'))}\n\n"
               f"**Needs evidence:**\n{_list(j.get('needs_evidence'))}\n\n"
               f"**Hidden assumptions:**\n{_list(j.get('hidden_assumptions'))}\n\n"
               f"**Take-away question:** {j.get('take_away_question','')}")
    out.append("\n## 6 · Questions & answers")
    for i, q in enumerate(d.questions):
        a = d.answers[i] if i < len(d.answers) else ""
        out.append(f"**Q{i+1}.** {q}  \n**A.** {a or '-'}")
    if r:
        out.append(f"\n## 7 · Reassess\n{r.get('feedback','')}\n\n**Survived:**\n{_list(r.get('survived'))}"
                   f"\n\n**Needs evidence:**\n{_list(r.get('needs_evidence'))}\n\n"
                   f"**Unexamined:**\n{_list(r.get('unexamined'))}\n\n**Next step:** {r.get('next_step','')}")
    if change_mind:
        out.append(f"\n**What would change my mind:** {change_mind}")
    if d.sources:
        out.append("\n## Sources")
        out += [f"[{s['n']}] {s['title']}: {s['url']}" for s in d.sources]
    if d.pushback:
        out.append("\n## 8 · Pushback")
        for turn in d.pushback:
            who = "User" if turn["role"] == "user" else "Devil"
            meta = turn.get("meta", {})
            tag = f" *(new argument: {meta.get('new_argument')}, changed: {meta.get('position_changed')})*" \
                if meta else ""
            out.append(f"**{who}:** {turn['content']}{tag}")
    return "\n".join(out) + "\n"
