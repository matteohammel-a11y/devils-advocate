"""Devil's Advocate: an AI that disagrees well.

Run:  uv run streamlit run app.py
"""
from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor

import streamlit as st

# Secrets (Streamlit Cloud "Advanced settings" or .streamlit/secrets.toml) → environment,
# before the devil modules read their defaults.
try:
    for _k, _v in st.secrets.items():
        if isinstance(_v, (str, int, float, bool)):
            os.environ.setdefault(_k, str(_v))
except Exception:  # noqa: BLE001 (no secrets file is fine locally)
    pass

from devil import memory, pipeline, store  # noqa: E402
from devil.export import to_markdown  # noqa: E402
from devil.i18n import EXAMPLES, LANGUAGES, METHOD, t  # noqa: E402
from devil.llm import DEFAULT_API_KEY, DEFAULT_BASE_URL, DEFAULT_MODEL, LLM, list_ollama_models  # noqa: E402
from devil.search import DEFAULT_KEY as TAVILY_KEY  # noqa: E402
from devil.ui import (CSS, E, bullets, card, gauge, hero, items, linkify, pill,  # noqa: E402
                      sources_list, stepper)

PUBLIC = os.getenv("DA_PUBLIC", "").lower() in ("1", "true", "yes")

st.set_page_config(page_title="Devil's Advocate", page_icon="😈", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("lang", "en")
ss.setdefault("step", "home")          # home → confirm → arena
ss.setdefault("debate", None)
ss.setdefault("editing", False)
ss.setdefault("saved", False)
ss.setdefault("belief_input", "")


# ---- sidebar ---------------------------------------------------------------------------
with st.sidebar:
    codes = list(LANGUAGES)
    ss.lang = st.selectbox(
        "🌐 " + t("language", ss.lang), codes, index=codes.index(ss.lang),
        format_func=lambda c: f"{LANGUAGES[c]['flag']}  {LANGUAGES[c]['name']}")
    L = ss.lang

    pages = [t("nav_arena", L), t("nav_community", L)] + ([] if PUBLIC else [t("nav_history", L)]) \
        + [t("nav_method", L)]
    page = st.radio(" ", pages, label_visibility="collapsed")
    st.divider()

    speed = st.radio("🏎️ " + t("speed", L), ["fast", "thorough"], horizontal=True,
                     format_func=lambda m: t("speed_" + m, L))
    fast = speed == "fast"
    st.caption(t("speed_hint_" + speed, L))
    think = False

    if PUBLIC:
        # Public link: keys stay server-side (in secrets) and are never sent to the browser.
        base_url, api_key, model, temperature = DEFAULT_BASE_URL, DEFAULT_API_KEY, DEFAULT_MODEL, 0.4
        tavily_key = TAVILY_KEY
        web = st.toggle("🔎 " + t("web_search", L), value=bool(TAVILY_KEY), disabled=not TAVILY_KEY)
        st.caption(f"🧠 {model}")
    else:
        with st.expander("⚙️ " + t("connection", L), expanded=False):
            base_url = st.text_input("Base URL", DEFAULT_BASE_URL)
            api_key = st.text_input("API key", DEFAULT_API_KEY, type="password")
        models = list_ollama_models(base_url, api_key)
        if models:
            st.caption(f"🟢 {t('ollama_ok', L)} · {len(models)}")
            import re as _re

            def _ver(m):  # newest version first: gemini-3.8-flash before gemini-2.5-flash
                return [float(x) for x in _re.findall(r"\d+(?:\.\d+)?", m)] or [0.0]
            flash = sorted((m for m in models if "flash" in m and not any(
                x in m for x in ("lite", "preview", "image", "tts", "live", "exp"))), key=_ver, reverse=True)
            prefer = [DEFAULT_MODEL] + flash + [models[0]]
            default = models.index(next(m for m in prefer if m in models))
            model = st.selectbox("🧠 " + t("model", L), models, index=default)
        else:
            st.caption(f"🟠 {t('ollama_missing', L)}")
            model = st.text_input("🧠 " + t("model", L), DEFAULT_MODEL)
        temperature = st.slider("🌡️ " + t("temperature", L), 0.0, 1.2, 0.4, 0.1)
        think = st.toggle("🧠 " + t("deep_think", L), value=False, help=t("deep_think_help", L))

        web = st.toggle("🔎 " + t("web_search", L), value=bool(TAVILY_KEY))
        tavily_key = TAVILY_KEY
        if web:
            tavily_key = st.text_input(t("tavily_key", L), TAVILY_KEY, type="password",
                                       help=t("tavily_help", L), placeholder="tvly-…")
            if not tavily_key:
                st.caption("🟠 " + t("need_key", L))
    st.caption(("🗄️ " if store.backend() == "supabase" else "💾 ") + t("storage_" + store.backend(), L))

    st.divider()
    if st.button("✨ " + t("new_debate", L), use_container_width=True):
        for k in [k for k in ss if k in ("after", "change_mind", "rating", "feedback_text")
                  or (k[:1] == "a" and k[1:].isdigit())]:
            del ss[k]
        ss.debate, ss.editing, ss.saved = None, False, False
        ss.step, ss.belief_input = "home", ""
        st.rerun()

llm = LLM(model=model, base_url=base_url, api_key=api_key, temperature=temperature, think=think)
L = ss.lang


def explain(exc: Exception) -> str:
    """Turn API errors into a one-line hint."""
    code = getattr(exc, "status_code", None)
    hints = {401: "the API key is wrong", 403: "the API key isn't allowed to use this",
             402: "this provider needs paid credits", 503: "the model's server is overloaded. Try again or pick another model", 404: "this model doesn't exist (anymore). Pick another one",
             429: "the free limit was hit. Wait a minute and try again"}
    return f"{t('error', L)} ({code}: {hints[code]})" if code in hints else t("error", L)


def run(label: str, fn, *args) -> bool:
    """Run a pipeline stage with a status box; show a friendly error if it fails."""
    try:
        with st.status(label, expanded=False) as s:
            fn(*args)
            s.update(label=f"{label} ✓", state="complete")
        return True
    except Exception as exc:  # noqa: BLE001
        st.error(explain(exc))
        with st.expander("Details"):
            st.exception(exc)
        return False


def run_debate(d: pipeline.Debate) -> bool:
    """Advocate and Devil are built in parallel and independently, then rebuttal, then Judge."""
    t0 = time.perf_counter()
    try:
        with st.status(t("p_advocate", L) + "  ·  " + t("p_devil", L), expanded=True) as s:
            d.sources, d.search_error, d.rebuttals = [], "", {}
            if web and tavily_key:
                st.write("🔎 " + t("p_search", L))
                try:
                    pipeline.research(d, tavily_key)
                    st.write(f"   ↳ {len(d.sources)} {t('sources', L).lower()}")
                except Exception as exc:  # noqa: BLE001 (search failing must not kill the debate)
                    d.search_error = str(exc)
            d.examples = store.best_examples(d.restatement)
            if d.examples:
                st.write("📚 " + t("learned_from", L).format(n=len(d.examples)))
            st.write("⚖️ " + t("p_advocate", L))
            st.write("😈 " + t("p_devil", L))
            with ThreadPoolExecutor(max_workers=2) as pool:
                fa = pool.submit(pipeline.advocate, llm, d)
                fd = pool.submit(pipeline.devil, llm, d, fast)
                fa.result(), fd.result()
            if not fast:
                st.write("🔁 " + t("p_rebuttal", L))
                pipeline.rebuttal(llm, d)
            st.write("🧑‍⚖️ " + t("p_judge", L))
            pipeline.judge(llm, d)
            s.update(label=f"{t('p_done', L)} ✓ · {time.perf_counter() - t0:.0f}s", state="complete",
                     expanded=False)
        persist(d, new=True)
        return True
    except Exception as exc:  # noqa: BLE001
        st.error(explain(exc))
        with st.expander("Details"):
            st.exception(exc)
        return False


def persist(d: pipeline.Debate, new: bool = False, **extra) -> None:
    """Save the debate to shared storage. Storage problems never break the app."""
    try:
        if new or not d.db_id:
            d.db_id = store.save({
                "language": d.language, "model": model, "belief": d.belief, "restatement": d.restatement,
                "claim_type": d.understanding.get("claim_type"), "confidence_before": d.confidence,
                "advocate": d.advocate, "challenge": d.challenge, "steelman": d.oppose.get("steelman", ""),
                "questions": d.questions, "judge": d.judge, "sources": d.sources})
        else:
            store.update(d.db_id, extra)
    except Exception as exc:  # noqa: BLE001
        st.caption(f"⚠️ storage: {str(exc)[:120]}")


# ---- pages -------------------------------------------------------------------------------
def page_home() -> None:
    st.markdown(stepper(0, L), unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 3, 1])
    with mid:
        st.markdown(f"<h2 style='text-align:center;margin-bottom:.6rem'>{E(t('what_believe', L))}</h2>",
                    unsafe_allow_html=True)
        belief = st.text_area(" ", key="belief_input", placeholder=t("placeholder", L), height=110,
                              label_visibility="collapsed")
        conf = st.slider(t("how_sure", L), 0, 100, 70)
        if st.button("😈  " + t("challenge_me", L), type="primary", use_container_width=True):
            if not belief.strip():
                st.warning(t("empty_belief", L))
            else:
                d = pipeline.Debate(belief=belief.strip(), confidence=conf,
                                    language=LANGUAGES[L]["name"])
                if run(t("p_understand", L), pipeline.understand, llm, d):
                    ss.debate, ss.step, ss.saved = d, "confirm", False
                    st.rerun()

        st.caption("🔒 " + t("consent", L))
        st.markdown(f"<p class='muted' style='text-align:center;margin-top:1.4rem'>"
                    f"{E(t('or_try', L))}</p>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, ex in enumerate(EXAMPLES[L]):
            cols[i % 2].button(ex, key=f"ex{i}", use_container_width=True,
                               on_click=lambda ex=ex: ss.update(belief_input=ex))


def page_confirm(d: pipeline.Debate) -> None:
    st.markdown(stepper(0, L), unsafe_allow_html=True)
    u = d.understanding
    tags = f'<span class="pill tag">{E(t("type", L))}: {E(u.get("claim_type", "?"))}</span>'
    if u.get("false_premise", {}).get("flag"):
        tags += f'<span class="pill unsupported" style="margin-left:0;margin-right:.35rem">⚠ ' \
                f'{E(t("flag_false_premise", L))}</span>'
    if u.get("near_consensus", {}).get("flag"):
        tags += f'<span class="pill supported" style="margin-left:0">✓ {E(t("flag_consensus", L))}</span>'
    notes = "".join(f'<p class="muted">{E(u[k]["note"])}</p>' for k in ("false_premise", "near_consensus")
                    if u.get(k, {}).get("flag") and u[k].get("note"))
    body = (f'<p class="muted">“{E(d.belief)}” · {d.confidence}/100</p>'
            f'<div class="quote">{E(d.restatement)}</div><div>{tags}</div>{notes}'
            f'<p class="muted" style="margin-top:.8rem">ⓘ {E(t("understand_hint", L))}</p>')
    _, mid, _ = st.columns([1, 4, 1])
    with mid:
        st.markdown(card("neutral", "Stage 1 · " + t("s_understand", L), t("did_i_get", L), body),
                    unsafe_allow_html=True)
        if ss.editing:
            new = st.text_area(t("edit_it", L), d.restatement, height=90)
            if st.button(t("save_edit", L), type="primary"):
                d.restatement, ss.editing = new.strip() or d.restatement, False
                st.rerun()
        else:
            c1, c2 = st.columns([2, 1])
            if c1.button("⚔️  " + t("yes_go", L), type="primary", use_container_width=True):
                if run_debate(d):
                    ss.step = "arena"
                    st.rerun()
            if c2.button("✏️  " + t("edit_it", L), use_container_width=True):
                ss.editing = True
                st.rerun()


def render_advocate(d: pipeline.Debate) -> str:
    a = d.advocate
    args = items([(x.get("claim", ""), x.get("reasoning", ""), pill(x.get("evidence"), L))
                  for x in a.get("arguments", [])])
    body = (f'<p>{E(a.get("summary", ""))}</p><h4>{E(t("arguments", L))}</h4>{args}'
            f'<h4>{E(t("unmentioned", L))}</h4>{bullets(a.get("unmentioned_reasons"))}')
    return card("adv", "⚖️ " + t("advocate", L), t("your_case", L), body)


def render_devil(d: pipeline.Debate) -> str:
    ch, op = d.challenge, d.oppose
    assumptions = items([(x.get("assumption", ""), f'{t("if_false", L)}: {x.get("why_load_bearing", "")}',
                          pill(x.get("evidence"), L)) for x in ch.get("assumptions", [])])
    claims = items([(x.get("claim", ""), x.get("note", ""), pill(x.get("evidence"), L))
                    for x in ch.get("claims", [])])
    body = (f'<h4>{E(t("weak_assumptions", L))}</h4>{assumptions}'
            f'<h4>{E(t("steelman", L))}</h4><div class="steel">{E(op.get("steelman", ""))}</div>'
            f'{bullets(op.get("key_points"))}'
            f'<h4>{E(t("claims_checked", L))}</h4>{claims}')
    return card("dev", "😈 " + t("devil", L), t("other_side", L), body)


def render_rebuttals(d: pipeline.Debate) -> None:
    if not d.rebuttals:
        return
    with st.expander("🔁  " + t("rebuttals", L)):
        c1, c2 = st.columns(2)
        for col, side, cls in ((c1, "advocate", "adv"), (c2, "devil", "dev")):
            rb = d.rebuttals.get(side, {})
            conc = rb.get("concessions") or []
            col.markdown(
                f'<span class="pill {cls}">{E(t(side, L))}</span><p style="margin-top:.5rem">'
                f'{E(rb.get("rebuttal", ""))}</p>'
                + (f'<p class="muted"><b>{E(t("concedes", L))}:</b> {E("; ".join(conc))}</p>' if conc else ""),
                unsafe_allow_html=True)


def render_judge(d: pipeline.Debate) -> str:
    j = d.judge
    grid = (f'<div class="map">'
            f'<div class="col ok"><div class="h">✓ {E(t("survived", L))}</div>{bullets(j.get("survived"))}</div>'
            f'<div class="col ev"><div class="h">? {E(t("needs_evidence", L))}</div>'
            f'{bullets(j.get("needs_evidence"))}</div>'
            f'<div class="col hid"><div class="h">◌ {E(t("hidden", L))}</div>'
            f'{bullets(j.get("hidden_assumptions"))}</div></div>')
    take = (f'<div class="takeaway">💭 <span class="muted" style="font-family:Inter">'
            f'{E(t("takeaway", L))}:</span><br>{E(j.get("take_away_question", ""))}</div>')
    rows = "".join(
        f'<tr><td style="width:110px"><span class="pill {"adv" if c.get("side") == "advocate" else "dev"}">'
        f'{E(t("advocate" if c.get("side") == "advocate" else "devil", L))}</span></td>'
        f'<td>{E(c.get("claim", ""))}</td><td style="text-align:right">'
        f'{pill(c.get("verdict"), L, "v_")}</td></tr>' for c in j.get("claim_map", []))
    table = f'<h4>{E(t("claim_map", L))}</h4><table class="claims">{rows}</table>' if rows else ""
    return card("jud", "🧑‍⚖️ " + t("judge", L) + " · blinded", t("the_map", L),
                f'<p class="muted">{E(t("no_winner", L))}</p>{grid}{take}{table}')


def page_arena(d: pipeline.Debate) -> None:
    st.markdown(stepper(4 if d.reassess else 3, L), unsafe_allow_html=True)
    st.markdown(f'<div class="card neutral"><div class="kicker">{E(t("s_understand", L))}</div>'
                f'<div class="quote" style="margin:0">{E(d.restatement)}</div>'
                + ("".join(f'<span class="pill tag" style="margin-top:.6rem">skill · {E(s)}</span>'
                           for s in d.skills_used)) + "</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    c1.markdown(linkify(render_advocate(d), d.sources), unsafe_allow_html=True)
    c2.markdown(linkify(render_devil(d), d.sources), unsafe_allow_html=True)
    render_rebuttals(d)
    st.markdown(linkify(render_judge(d), d.sources), unsafe_allow_html=True)
    if d.sources:
        with st.expander(f"🔎  {t('sources', L)} ({len(d.sources)})"):
            st.markdown(f'<p class="muted">{E(t("sources_hint", L))}</p>' + sources_list(d.sources),
                        unsafe_allow_html=True)
    elif d.search_error:
        st.caption(f"⚠️ {t('search_failed', L)}: {d.search_error[:160]}")

    # ---- feedback → powers the learning loop
    with st.container(border=True):
        st.markdown(f"**{t('rate_q', L)}**  \n<span class='muted'>{E(t('rate_hint', L))}</span>",
                    unsafe_allow_html=True)
        fc1, fc2 = st.columns([1, 4])
        with fc1:
            rating = st.feedback("thumbs", key="rating")
        fb = fc2.text_input(" ", key="feedback_text", placeholder=t("feedback_ph", L),
                            label_visibility="collapsed")
        if rating is not None and ss.get("rated") != (d.db_id, rating, fb):
            persist(d, rating=int(rating), feedback=fb)
            ss.rated = (d.db_id, rating, fb)
            st.toast(t("thanks", L), icon="🙏")

    # ---- Stage 4: questions
    st.markdown(f"### 😈 {E(t('your_turn', L))}", unsafe_allow_html=True)
    with st.form("answers"):
        answers = [st.text_area(f"**{i+1}.** {q}", key=f"a{i}", placeholder=t("answer_here", L), height=80)
                   for i, q in enumerate(d.questions)]
        submitted = st.form_submit_button("🔍  " + t("submit_answers", L), type="primary")
    if submitted:
        d.answers = answers
        if run(t("p_reassess", L), pipeline.reassess, llm, d):
            persist(d, answers=d.answers, reassess=d.reassess)
            st.rerun()

    # ---- Stage 5: reassess
    if d.reassess:
        r = d.reassess
        grid = (f'<p>{E(r.get("feedback", ""))}</p><div class="map">'
                f'<div class="col ok"><div class="h">✓ {E(t("survived", L))}</div>{bullets(r.get("survived"))}</div>'
                f'<div class="col ev"><div class="h">? {E(t("needs_evidence", L))}</div>'
                f'{bullets(r.get("needs_evidence"))}</div>'
                f'<div class="col hid"><div class="h">◌ {E(t("unexamined", L))}</div>'
                f'{bullets(r.get("unexamined"))}</div></div>'
                f'<div class="takeaway">🧭 <span class="muted" style="font-family:Inter">{E(t("next_step", L))}:'
                f'</span><br>{E(r.get("next_step", ""))}</div>')
        st.markdown(card("neutral", "Stage 5 · " + t("s_reassess", L), t("reassessment", L), grid),
                    unsafe_allow_html=True)
        after = st.slider(t("conf_now", L), 0, 100, d.confidence, key="after")
        st.markdown(gauge(d.confidence, after, L), unsafe_allow_html=True)
        change = st.text_area(t("change_mind", L), key="change_mind", height=80)
        c1, c2 = st.columns(2)
        if c1.button("💾  " + t("save_session", L), use_container_width=True, disabled=ss.saved):
            persist(d, confidence_after=after, change_mind=change)
            if not PUBLIC:
                    memory.remember({"belief": d.belief, "restatement": d.restatement, "before": d.confidence,
                                 "after": after, "takeaway": d.judge.get("take_away_question", ""),
                                 "change_mind": change, "language": d.language, "model": model})
            ss.saved = True
            st.toast(t("saved", L), icon="💾")
        c2.download_button("⬇️  " + t("download", L), to_markdown(d, model, after, change),
                           file_name="devils_advocate_debate.md", use_container_width=True)

    # ---- pushback chat
    st.markdown(f"### 🥊 {E(t('push_title', L))}")
    st.caption(t("push_hint", L))
    for turn in d.pushback:
        with st.chat_message("user" if turn["role"] == "user" else "assistant",
                             avatar="🙂" if turn["role"] == "user" else "😈"):
            st.write(turn["content"])
            meta = turn.get("meta")
            if meta:
                moved = meta.get("position_changed")
                st.markdown(
                    f'<div class="verdict">{"🔄 " + E(t("moved", L)) if moved else "🛡️ " + E(t("held", L))}'
                    f' · {E(t("new_arg", L) if meta.get("new_argument") else t("no_new_arg", L))}'
                    + (f' · {E(meta.get("what_changed"))}' if moved and meta.get("what_changed") else "")
                    + "</div>", unsafe_allow_html=True)
    with st.form("pushback", clear_on_submit=True):
        c1, c2 = st.columns([6, 1])
        msg = c1.text_input(" ", placeholder=t("push_placeholder", L), label_visibility="collapsed",
                            key="push_msg")
        sent = c2.form_submit_button("🥊", use_container_width=True)
    if sent and msg.strip():
        try:
            with st.spinner("😈 …"):
                pipeline.push_back(llm, d, msg)
            persist(d, pushback=[{k: v for k, v in turn.items()} for turn in d.pushback])
            st.rerun()
        except Exception as exc:  # noqa: BLE001
            st.error(t("error", L))
            st.exception(exc)


def page_history() -> None:
    st.markdown(f"## 📚 {E(t('nav_history', L))}")
    hist = memory.load_history()
    if not hist:
        st.info(t("history_empty", L))
        return
    for h in reversed(hist):
        body = (f'<p class="muted">{E(h.get("date", ""))} · {E(h.get("model", ""))} · {E(h.get("language", ""))}</p>'
                f'{gauge(int(h.get("before", 0)), int(h.get("after", 0)), L)}'
                f'<div class="takeaway" style="font-size:1rem">💭 {E(h.get("takeaway", ""))}</div>'
                + (f'<p style="margin-top:.7rem"><b>{E(t("change_mind", L))}</b> {E(h["change_mind"])}</p>'
                   if h.get("change_mind") else ""))
        st.markdown(card("neutral", t("confidence", L), h.get("belief", ""), body), unsafe_allow_html=True)
    if st.button("🗑️ " + t("clear_history", L)):
        memory.clear()
        st.rerun()


def page_community() -> None:
    st.markdown(f"## 🌍 {E(t('nav_community', L))}")
    st.caption(t("community_hint", L))
    try:
        rows = store.recent(300)
    except Exception as exc:  # noqa: BLE001
        st.error(f"Storage: {exc}")
        return
    if not rows:
        st.info(t("no_debates", L))
        return
    rated = [r for r in rows if r.get("rating") is not None]
    shifts = [abs(r["confidence_after"] - r["confidence_before"]) for r in rows
              if r.get("confidence_after") is not None and r.get("confidence_before") is not None]
    m = st.columns(4)
    m[0].metric(t("m_debates", L), len(rows))
    m[1].metric(t("m_useful", L), f"{100 * sum(r['rating'] for r in rated) / len(rated):.0f}%" if rated else "–")
    m[2].metric(t("m_shift", L), f"{sum(shifts) / len(shifts):.0f} pts" if shifts else "–")
    m[3].metric(t("m_languages", L), len({r.get("language") for r in rows}))

    for r in rows[:25]:
        emoji = {1: "👍", 0: "👎"}.get(r.get("rating"), "·")
        after = r.get("confidence_after")
        body = (f'<p class="muted">{E((r.get("created_at") or "")[:16].replace("T", " "))} · '
                f'{E(r.get("language") or "")} · {emoji}</p>'
                f'<div class="quote" style="font-size:1.1rem">{E(r.get("restatement") or "")}</div>'
                + (gauge(int(r.get("confidence_before") or 0), int(after), L) if after is not None else "")
                + f'<div class="takeaway" style="font-size:1rem">💭 '
                  f'{E((r.get("judge") or {}).get("take_away_question", ""))}</div>'
                + (f'<p class="muted" style="margin-top:.6rem">💬 {E(r["feedback"])}</p>' if r.get("feedback") else ""))
        st.markdown(card("neutral", t("confidence", L), r.get("belief") or "", body), unsafe_allow_html=True)

    # Team export (password-protected when ADMIN_PASSWORD is set)
    with st.expander("🔐 " + t("team_export", L)):
        pw = os.getenv("ADMIN_PASSWORD", "")
        if pw and st.text_input(t("admin_pw", L), type="password") != pw:
            return
        import csv
        import io
        import json as _json
        buf = io.StringIO()
        cols = ["created_at", "language", "model", "belief", "restatement", "claim_type", "confidence_before",
                "confidence_after", "rating", "feedback", "steelman", "questions", "answers", "judge",
                "reassess", "pushback", "sources", "change_mind"]
        w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({c: (_json.dumps(r.get(c), ensure_ascii=False) if isinstance(r.get(c), (dict, list))
                            else r.get(c)) for c in cols})
        st.download_button("⬇️ CSV", buf.getvalue(), "devils_advocate_debates.csv", "text/csv")


def page_method() -> None:
    st.markdown(f"## 🧭 {E(t('nav_method', L))}")
    c1, c2 = st.columns([3, 2], gap="large")
    c1.markdown(METHOD[L])
    flow = [("1", t("s_understand", L), "neutral"), ("2", f"{t('advocate', L)} ‖ {t('devil', L)}", "dev"),
            ("3", t("rebuttals", L), "neutral"), ("4", t("judge", L) + " · blinded", "jud"),
            ("5", f"{t('s_question', L)} → {t('s_reassess', L)}", "adv")]
    c2.markdown("".join(
        f'<div class="card {cls}" style="padding:.9rem 1.1rem"><div class="kicker">Stage {n}</div>'
        f'<div style="font-family:Fraunces;font-size:1.15rem">{E(name)}</div></div>'
        + ('<div style="text-align:center;color:var(--muted)">↓</div>' if n != "5" else "")
        for n, name, cls in flow), unsafe_allow_html=True)


# ---- router ------------------------------------------------------------------------------
st.markdown(hero(L), unsafe_allow_html=True)
if page == t("nav_history", L):
    page_history()
elif page == t("nav_community", L):
    page_community()
elif page == t("nav_method", L):
    page_method()
elif ss.step == "confirm" and ss.debate:
    page_confirm(ss.debate)
elif ss.step == "arena" and ss.debate:
    page_arena(ss.debate)
else:
    page_home()
