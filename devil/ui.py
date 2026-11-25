"""Visual layer: CSS theme and small HTML components (all model text is escaped)."""
from __future__ import annotations

import re
from html import escape
from urllib.parse import urlparse

from .i18n import t

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap');

:root{
  --bg:#0B0D12; --surface:#141821; --surface2:#1B2030; --border:#262C3D;
  --text:#ECEAE4; --muted:#9AA3B5;
  --adv:#4EA8FF; --adv-soft:rgba(78,168,255,.12);
  --dev:#FF4D5E; --dev-soft:rgba(255,77,94,.12);
  --jud:#F5C04A; --jud-soft:rgba(245,192,74,.12);
  --ok:#3DDC97; --ok-soft:rgba(61,220,151,.12);
  --warn:#F5A524; --warn-soft:rgba(245,165,36,.12);
}
html, body, [class*="css"], .stMarkdown, p, li, label, input, textarea { font-family:'Inter',sans-serif; }
.stApp { background: radial-gradient(1200px 600px at 10% -10%, rgba(78,168,255,.07), transparent 60%),
                     radial-gradient(1000px 500px at 100% 0%, rgba(255,77,94,.08), transparent 60%), var(--bg); }
.block-container { max-width: 1180px; padding-top: 2.2rem; }
h1,h2,h3,h4 { font-family:'Fraunces',serif !important; letter-spacing:-.01em; }

/* hero */
.hero { text-align:center; margin: .4rem 0 1.6rem; }
.hero .mark { font-size:2.6rem; line-height:1; }
.hero h1 { font-size:3.1rem; margin:.3rem 0 .2rem; font-weight:700;
  background: linear-gradient(90deg, var(--adv) 0%, #c9b8ff 45%, var(--dev) 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent; }
.hero p { color:var(--muted); font-size:1.05rem; margin:0; }

/* stepper */
.stepper { display:flex; gap:.5rem; justify-content:center; flex-wrap:wrap; margin: 0 0 1.6rem; }
.step { display:flex; align-items:center; gap:.45rem; padding:.38rem .8rem; border-radius:999px;
  border:1px solid var(--border); color:var(--muted); font-size:.82rem; background:var(--surface); }
.step .n { width:1.35rem; height:1.35rem; border-radius:50%; display:grid; place-items:center;
  font-family:'JetBrains Mono',monospace; font-size:.72rem; background:var(--surface2); }
.step.done { color:var(--ok); border-color:rgba(61,220,151,.35); }
.step.done .n { background:var(--ok-soft); }
.step.active { color:var(--text); border-color:#c9b8ff; box-shadow:0 0 0 3px rgba(201,184,255,.12); }
.step.active .n { background:#c9b8ff; color:#111; }

/* cards */
.card { background:var(--surface); border:1px solid var(--border); border-radius:18px;
  padding:1.25rem 1.35rem; margin-bottom:1rem; position:relative; overflow:hidden; }
.card::before { content:""; position:absolute; inset:0 0 auto 0; height:3px; background:var(--accent,#c9b8ff); }
.card.adv { --accent:var(--adv); background:linear-gradient(180deg,var(--adv-soft),transparent 40%),var(--surface); }
.card.dev { --accent:var(--dev); background:linear-gradient(180deg,var(--dev-soft),transparent 40%),var(--surface); }
.card.jud { --accent:var(--jud); background:linear-gradient(180deg,var(--jud-soft),transparent 30%),var(--surface); }
.card.neutral { --accent:#c9b8ff; }
.card .kicker { font-family:'JetBrains Mono',monospace; font-size:.72rem; letter-spacing:.12em;
  text-transform:uppercase; color:var(--accent); margin-bottom:.35rem; }
.card h3 { margin:.1rem 0 .7rem; font-size:1.35rem; }
.card h4 { margin:1rem 0 .45rem; font-size:1rem; color:var(--muted); font-family:'Inter',sans-serif !important;
  font-weight:600; text-transform:uppercase; letter-spacing:.06em; font-size:.78rem; }
.card p { margin:.2rem 0 .5rem; line-height:1.55; }
.quote { font-family:'Fraunces',serif; font-size:1.35rem; line-height:1.45; margin:.2rem 0 .6rem; }

.item { padding:.7rem .85rem; border-radius:12px; background:var(--surface2); border:1px solid var(--border);
  margin:.45rem 0; }
.item .title { font-weight:600; margin-bottom:.2rem; }
.item .sub { color:var(--muted); font-size:.9rem; line-height:1.45; }
.steel { border-left:3px solid var(--dev); padding:.2rem 0 .2rem .9rem; font-size:1.02rem; line-height:1.6; }

/* pills */
.pill { display:inline-block; padding:.12rem .55rem; border-radius:999px; font-size:.72rem; font-weight:600;
  font-family:'JetBrains Mono',monospace; margin-left:.35rem; vertical-align:middle; white-space:nowrap; }
.pill.supported, .pill.well_supported { color:var(--ok); background:var(--ok-soft); }
.pill.contested, .pill.untested_assumption { color:var(--warn); background:var(--warn-soft); }
.pill.unsupported, .pill.asserted { color:var(--dev); background:var(--dev-soft); }
.pill.tag { color:#c9b8ff; background:rgba(201,184,255,.12); margin-left:0; margin-right:.35rem; }
.pill.adv { color:var(--adv); background:var(--adv-soft); margin-left:0; }
.pill.dev { color:var(--dev); background:var(--dev-soft); margin-left:0; }

/* map grid */
.map { display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; }
@media (max-width: 900px){ .map{ grid-template-columns:1fr; } }
.map .col { background:var(--surface2); border:1px solid var(--border); border-radius:14px; padding:.9rem 1rem; }
.map .col .h { font-weight:600; font-size:.85rem; margin-bottom:.5rem; display:flex; gap:.45rem; align-items:center; }
.map .col ul { margin:0; padding-left:1.1rem; } .map .col li { margin:.3rem 0; line-height:1.45; }
.map .ok .h { color:var(--ok); } .map .ev .h { color:var(--warn); } .map .hid .h { color:var(--dev); }
.takeaway { margin-top:.9rem; padding:1rem 1.1rem; border-radius:14px; border:1px dashed var(--jud);
  background:var(--jud-soft); font-family:'Fraunces',serif; font-size:1.15rem; }
table.claims { width:100%; border-collapse:collapse; margin-top:.4rem; font-size:.92rem; }
table.claims, table.claims tr, table.claims td { border:none !important; background:transparent !important; }
table.claims td { padding:.55rem .4rem; border-top:1px solid var(--border) !important; vertical-align:top; }
[data-testid="stHeaderActionElements"], .card h3 a { display:none !important; }

/* confidence gauge */
.gauge { margin:.6rem 0 .2rem; }
.gauge .track { position:relative; height:12px; border-radius:999px;
  background:linear-gradient(90deg,#2a3042,#3a4157); }
.gauge .fill { position:absolute; top:0; bottom:0; border-radius:999px; opacity:.55; }
.gauge .dot { position:absolute; top:50%; width:20px; height:20px; border-radius:50%; transform:translate(-50%,-50%);
  border:3px solid var(--bg); }
.gauge .legend { display:flex; justify-content:space-between; color:var(--muted); font-size:.82rem; margin-top:.55rem; }
.delta { font-family:'JetBrains Mono',monospace; font-weight:600; }

/* citations & sources */
a.cite { color:#c9b8ff; text-decoration:none; font-family:'JetBrains Mono',monospace; font-size:.8em;
  padding:0 .15rem; border-radius:4px; background:rgba(201,184,255,.12); }
a.cite:hover { background:rgba(201,184,255,.3); }
.src { display:flex; gap:.7rem; padding:.6rem .2rem; border-top:1px solid var(--border); }
.src .num { font-family:'JetBrains Mono',monospace; color:#c9b8ff; min-width:1.8rem; }
.src a { color:var(--text); font-weight:600; text-decoration:none; } .src a:hover { text-decoration:underline; }
.src .dom { color:var(--muted); font-size:.8rem; }
.src .snip { color:var(--muted); font-size:.86rem; line-height:1.45; margin-top:.15rem; }

/* chat badges */
.verdict { font-size:.78rem; margin-top:.35rem; color:var(--muted); }

/* widgets */
.stButton>button, .stFormSubmitButton>button, .stDownloadButton>button { border-radius:12px; font-weight:600; padding:.55rem 1.1rem; }
.stButton>button[kind="primary"], .stFormSubmitButton>button[kind="primary"] {
  background:linear-gradient(90deg,#ff4d5e,#ff7a59); border:0; color:white; }
textarea, .stTextInput input { border-radius:12px !important; }
[data-testid="stSidebar"] { background:#0F121A; border-right:1px solid var(--border); }
.muted { color:var(--muted); font-size:.9rem; }
</style>
"""

E = escape


def pill(kind: str, lang: str, prefix: str = "e_") -> str:
    kind = (kind or "").strip().lower().replace(" ", "_")
    return f'<span class="pill {E(kind)}">{E(t(prefix + kind, lang) if kind else "?")}</span>'


def hero(lang: str) -> str:
    return (f'<div class="hero"><div class="mark">😈</div><h1>Devil\'s Advocate</h1>'
            f'<p>{E(t("tagline", lang))}</p></div>')


def stepper(active: int, lang: str) -> str:
    keys = ["s_understand", "s_debate", "s_judge", "s_question", "s_reassess"]
    out = []
    for i, k in enumerate(keys):
        cls = "done" if i < active else "active" if i == active else ""
        out.append(f'<div class="step {cls}"><span class="n">{i+1}</span>{E(t(k, lang))}</div>')
    return '<div class="stepper">' + "".join(out) + "</div>"


def card(kind: str, kicker: str, title: str, body: str) -> str:
    return (f'<div class="card {kind}"><div class="kicker">{E(kicker)}</div>'
            f'<h3>{E(title)}</h3>{body}</div>')


def items(rows: list[tuple[str, str, str]]) -> str:
    """rows: (title, sub, pill_html)"""
    return "".join(f'<div class="item"><div class="title">{E(a)}{p}</div>'
                   + (f'<div class="sub">{E(b)}</div>' if b else "") + "</div>" for a, b, p in rows)


def bullets(xs: list) -> str:
    xs = [x for x in xs or [] if isinstance(x, str) and x.strip()]
    return "<ul>" + "".join(f"<li>{E(x)}</li>" for x in xs) + "</ul>" if xs else '<p class="muted">-</p>'


def gauge(before: int, after: int | None, lang: str) -> str:
    lo, hi = sorted([before, after if after is not None else before])
    fill = (f'<div class="fill" style="left:{lo}%;width:{hi-lo}%;background:#c9b8ff"></div>'
            if after is not None else "")
    dots = f'<div class="dot" style="left:{before}%;background:var(--adv)"></div>'
    if after is not None:
        dots += f'<div class="dot" style="left:{after}%;background:var(--dev)"></div>'
    delta = ""
    if after is not None:
        d = after - before
        color = "var(--muted)" if d == 0 else ("var(--ok)" if abs(d) >= 1 else "var(--muted)")
        delta = f'<span class="delta" style="color:{color}">{"+" if d > 0 else ""}{d}</span>'
    after_txt = f"{t('after', lang)}: <b>{after}</b>" if after is not None else ""
    return (f'<div class="gauge"><div class="track">{fill}{dots}</div>'
            f'<div class="legend"><span>● <span style="color:var(--adv)">{E(t("before", lang))}</span>: '
            f'<b>{before}</b></span>{delta}<span><span style="color:var(--dev)">●</span> {after_txt}</span>'
            f"</div></div>")


def linkify(html: str, sources: list[dict]) -> str:
    """Turn [n] in already-escaped HTML into links to source n."""
    urls = {str(s["n"]): s["url"] for s in sources or []}
    if not urls:
        return html
    def sub(m):
        n = m.group(1)
        return f'<a class="cite" href="{E(urls[n])}" target="_blank">[{n}]</a>' if n in urls else m.group(0)
    return re.sub(r"\[(\d{1,2})\]", sub, html)


def sources_list(sources: list[dict]) -> str:
    rows = []
    for s in sources:
        dom = urlparse(s["url"]).netloc.removeprefix("www.")
        rows.append(f'<div class="src"><div class="num">[{s["n"]}]</div><div>'
                    f'<a href="{E(s["url"])}" target="_blank">{E(s["title"] or dom)}</a>'
                    f' <span class="dom">· {E(dom)}</span>'
                    f'<div class="snip">{E(s["content"][:220])}…</div></div></div>')
    return "".join(rows)
