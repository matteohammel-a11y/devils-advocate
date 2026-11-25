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
