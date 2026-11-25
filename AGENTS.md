# Context for coding agents (OpenCode)

This is "Devil's Advocate", a Streamlit app that stress-tests a user's belief with an Advocate / Devil /
blinded Judge pipeline running on local Ollama models.

- Run: `uv run streamlit run app.py`. Tests: `uv run pytest -q` (they use `tests/fake_llm.py`, no Ollama needed).
- Agent behaviour lives in `prompts/*.md` and `system.md`; placeholders are `{{name}}`. Every prompt returns JSON.
- Skills in `skills/` are injected only when Stage 1 flags them (`Debate.skills()` in `devil/pipeline.py`).
- **Invariant:** the Judge must never receive `Debate.belief` or `Debate.confidence`, only the neutral restatement.
  `tests/test_pipeline.py::test_judge_is_blinded` enforces this.
- All UI text goes through `devil/i18n.py` (`t(key, lang)`); add every new string in all 5 languages.
- Model output rendered as HTML must be escaped (`devil/ui.py` → `E()`).
- Keep the dark theme palette in `devil/ui.py` (`--adv` blue, `--dev` red, `--jud` gold).
