import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fake_llm import FakeLLM  # noqa: E402

from devil import pipeline  # noqa: E402
from devil.export import to_markdown  # noqa: E402
from devil.llm import parse_json  # noqa: E402


def full_run():
    llm = FakeLLM()
    d = pipeline.Debate("I'm absolutely certain a master's is better than working.", 90)
    pipeline.understand(llm, d)
    pipeline.advocate(llm, d)
    pipeline.devil(llm, d)
    pipeline.rebuttal(llm, d)
    pipeline.judge(llm, d)
    d.answers = ["Probably not.", "Consulting roles."]
    pipeline.reassess(llm, d)
    pipeline.push_back(llm, d, "I really don't think so.")
    return llm, d


def test_full_pipeline():
    llm, d = full_run()
    assert d.restatement.startswith("A master's")
    assert len(d.challenge["assumptions"]) == 3
    assert d.questions and d.judge["survived"] and d.reassess["next_step"]
    assert d.pushback[-1]["meta"]["position_changed"] is False


def test_judge_is_blinded():
    llm, d = full_run()
    judge_prompt = next(c for c in llm.calls if "# Role — Judge" in c)
    assert d.belief not in judge_prompt and "absolutely certain" not in judge_prompt
    assert "90" not in judge_prompt.split("# Role — Judge")[1]


def test_skill_loaded_only_when_needed():
    llm, d = full_run()
    assert d.skills_used == ["personal_decision"]
    adv_prompt = next(c for c in llm.calls if "# Role — Advocate" in c)
    assert "Skill: personal decision" in adv_prompt and "Skill: false premise" not in adv_prompt


def test_parse_json_tolerant():
    assert parse_json('<think>hm</think>```json\n{"a": 1}\n```') == {"a": 1}
    assert parse_json('Sure! {"a": [1, 2]} hope that helps') == {"a": [1, 2]}


def test_export():
    _, d = full_run()
    md = to_markdown(d, "fake", 60, "A strong offer")
    assert "## 5 · Judge" in md and "60/100" in md and "Pushback" in md


def test_web_search_feeds_sources_into_prompts(monkeypatch):
    from devil import search
    fake = [{"title": "OECD study", "url": "https://oecd.org/a", "content": "Masters premium varies."},
            {"title": "Dup", "url": "https://oecd.org/a", "content": "same url"},
            {"title": "Blog", "url": "https://blog.com/b", "content": "Experience matters."}]
    monkeypatch.setattr(search, "tavily_search", lambda q, key, n=4: fake)
    llm = FakeLLM()
    d = pipeline.Debate("A master's is better than working.", 70)
    pipeline.understand(llm, d)
    pipeline.research(d, "tvly-test")
    assert [s["n"] for s in d.sources] == [1, 2]  # de-duplicated, numbered
    pipeline.advocate(llm, d)
    pipeline.devil(llm, d)
    pipeline.rebuttal(llm, d)
    pipeline.judge(llm, d)
    for tag in ("# Role — Advocate", "# Role — Devil · Stage 2", "# Role — Judge"):
        prompt = next(c for c in llm.calls if tag in c)
        assert "[1] OECD study (https://oecd.org/a)" in prompt
    assert "https://blog.com/b" in to_markdown(d, "fake")


def test_linkify():
    from devil.ui import linkify
    html = linkify("Premium varies [1] but not [7].", [{"n": 1, "url": "https://x.org"}])
    assert 'href="https://x.org"' in html and "[7]" in html and html.count("<a") == 1


def test_store_and_learning_loop(tmp_path, monkeypatch):
    from devil import store
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.setattr(store, "LOCAL", tmp_path / "debates.json")
    a = store.save({"restatement": "Remote work lowers productivity.", "steelman": "Output data say otherwise."})
    store.save({"restatement": "Other.", "steelman": "Weak case."})
    store.update(a, {"rating": 1, "feedback": "sharp"})
    assert store.backend() == "local" and len(store.recent()) == 2
    ex = store.best_examples("A master's is better than working.")
    assert [e["id"] for e in ex] == [a]
    assert store.best_examples("Remote work lowers productivity.") == []  # never its own belief

    llm = FakeLLM()
    d = pipeline.Debate("A master's is better than working.", 70)
    pipeline.understand(llm, d)
    d.examples = ex
    pipeline.devil(llm, d)
    oppose = next(c for c in llm.calls if "# Role — Devil · Stage 3" in c)
    assert "Output data say otherwise." in oppose


def test_fast_mode_uses_one_devil_call():
    llm = FakeLLM()
    d = pipeline.Debate("A master's is better than working.", 70)
    pipeline.understand(llm, d)
    pipeline.devil(llm, d, fast=True)
    devil_calls = [c for c in llm.calls if "# Role — Devil" in c]
    assert len(devil_calls) == 1 and len(d.challenge["assumptions"]) == 3
    assert d.oppose["steelman"] and len(d.questions) == 2


def test_llm_finds_a_working_variant(monkeypatch):
    """Gemini-style: 503 for reasoning 'none'/'minimal', works with 'low'. Then remembered."""
    import httpx
    from openai import InternalServerError
    from devil import llm as L
    monkeypatch.setattr(L.time, "sleep", lambda s: None)
    L.LLM._variant_cache.clear()
    llm = L.LLM(model="g3", base_url="http://x/v1")
    seen = []

    class Resp:
        choices = [type("C", (), {"message": type("M", (), {"content": '{"ok": 1}'})()})()]

    def create(**kw):
        seen.append(kw.get("reasoning_effort"))
        if kw.get("reasoning_effort") in ("none", "minimal"):
            raise InternalServerError("503", response=httpx.Response(503, request=httpx.Request("POST", "http://x")),
                                      body=None)
        return Resp()
    llm.client.chat.completions.create = create
    assert llm.json("s", "u") == {"ok": 1}
    assert seen == ["none", "minimal", "low"]
    seen.clear()
    assert llm.json("s", "u2") == {"ok": 1}
    assert seen == ["low"]  # remembered: no probing the second time


def test_audit_end_to_end():
    from devil import experiment as ex
    beliefs = [b for b in ex.BELIEFS if b["id"] in ("B1", "B7")]
    todo = ex.jobs(beliefs, models=("m1", "m2"))
    assert len(todo) == 2 * 3 * 3 * 2
    got = {}
    ex.run_many(lambda m: FakeLLM(), todo, workers=3, on_row=lambda r: got.__setitem__(ex.job_key(r), r))
    rows = list(got.values())
    assert len(rows) == 36 and not any(r.get("error") for r in rows)
    assert any("certain" in r["user_message"] for r in rows)
    ex.rate_many(FakeLLM(), rows, workers=3)
    assert all(r["ai_disagreement"] is not None for r in rows)
    res = {r["version"]: r for r in ex.summary(rows)}
    assert res["V1"]["caved_pct"] == 100 and res["V4"]["caved_pct"] == 0  # fake: plain replies cave
    assert res["V4"]["disagreement_avg_0to3"] == 3 and res["V4"]["conviction_gap"] == 0
    assert ex.summary(rows, by=("model", "version"))[0]["model"] == "m1"
    # dataset round trip (resume) keeps everything
    back = ex.clean_loaded(ex.read_csv(ex.to_csv(rows, ex.DATASET_COLS)))
    assert len(back) == 36 and {ex.job_key(r) for r in back} == set(got)
    # human check: perfect copy of AI scores -> 100% agreement
    sheet, key = ex.human_sample(rows, n=10)
    by_job = {ex.job_key(r): r for r in rows}
    for h, k in zip(sheet, key):
        r = by_job[k["job"]]
        h.update({"assumptions_0to2": r["ai_assumptions"], "steelman_0to2": r["ai_steelman"],
                  "disagreement_0to3": r["ai_disagreement"], "caved_yes_no": "yes" if r["ai_caved"] else "no"})
    agree = {a["item"]: a for a in ex.human_vs_ai(rows, key, ex.read_csv(ex.to_csv(sheet).replace(",", ";")))}
    assert agree["caved"]["exact_agreement_pct"] == 100 and agree["disagreement"]["exact_agreement_pct"] == 100
