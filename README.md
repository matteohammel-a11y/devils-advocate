# 😈 Devil's Advocate: an AI that disagrees well

*Investigating with AI · group project · Matteo Hammel & team*

> Language models are trained to be liked. Being liked and being useful to think with are not the same thing.

You type a belief and how sure you are. Instead of agreeing with you, the system runs your belief through a
**five-stage pipeline with three separate agents**: an **Advocate** (your best case), a **Devil** (the
strongest case against), and a **blinded Judge** (a map of what holds up, with no score and no winner). You
then answer the Devil's questions, see what survived, and re-rate your confidence.

Built the way we did it in class: **OpenCode + Ollama (local models) + Streamlit**, with prompts as plain
`.md` files, cross-session memory in `memory.md`, and **skills loaded only when needed**.

---

## Quick start

```bash
# 1. Ollama running with a model (any chat model works; qwen3:8b or llama3.1:8b recommended)
ollama pull qwen3:8b

# 2. Run the app
uv run streamlit run app.py
```

Open http://localhost:8501. Choose the language and model in the sidebar.

**Not on Ollama?** Any OpenAI-compatible server works: set *Connection → Base URL / API key* in the
sidebar, or use the `DA_BASE_URL`, `DA_API_KEY` and `DA_MODEL` environment variables. This also lets you run
the same pipeline on another model for the cross-model test.

**Put it online with a public link + shared database:** see **[DEPLOY.md](DEPLOY.md)** (Streamlit Community
Cloud + Ollama Cloud + Supabase, all free). In public mode (`DA_PUBLIC=true`), keys stay server-side and
visitors only see the app.

---

## How it works

| Stage | What happens | Prompt file |
|---|---|---|
| **1 · Understand** | Neutral restatement, no evaluation. It classifies the claim and checks for a *false premise* or a *near-consensus* fact. **You confirm or correct it.** | `prompts/understand.md` |
| **2 · Advocate** | Strongest honest case **for** the belief, including reasons you didn't mention. | `prompts/advocate.md` |
| **2 · Devil: Challenge** | Three load-bearing assumptions. Every claim labelled *supported / contested / unsupported*. | `prompts/challenge.md` |
| **2 · Devil: Oppose** | A steelman a real opponent would sign. | `prompts/oppose.md` |
| **2 · Devil: Question** | 2–3 questions aimed at gaps and edge cases. | `prompts/question.md` |
| **3 · Rebuttal round** | Each side sees the other for the first time and replies once, with explicit concessions. | `prompts/rebuttal.md` |
| **4 · Judge (blinded)** | Sees **only** the neutral restatement and the two cases, never your wording or confidence. Produces a map: survived / needs evidence / hidden assumptions, plus a claim-by-claim verdict. | `prompts/judge.md` |
| **5 · Reassess** | Uses your answers to show what held up. You re-rate your confidence (before → after). | `prompts/reassess.md` |
| **Pushback** | Argue back. The Devil moves **only** for new arguments or evidence and says what changed. | `prompts/pushback.md` |

Advocate and Devil run **in parallel and independently**: neither sees the other's case before the rebuttal.

**Rules in every prompt** (`system.md`):
- **Concession rule:** the Devil concedes to arguments, never to insistence.
- **Proportionality rule:** no false balance against well-established facts.
- No fabricated statistics or sources; "unsupported" ≠ "false".

**Skills (`skills/`) are loaded only when Stage 1 says they are needed:**
- `false_premise.md`: flag the myth before debating the conclusion
- `near_consensus.md`: don't manufacture a debate that doesn't exist
- `personal_decision.md`: averages ≠ your case; opportunity cost, reversibility

**Shared storage & learning loop:** every debate is saved (Supabase online, `debates.json` locally).
Users rate each challenge 👍/👎. Top-rated past challenges are shown to the Devil as examples for new
beliefs. The **Community** page shows live stats, and the team can export all debates as CSV.

**Personal memory:** "Save to my history" appends the belief, the confidence before and after, the take-away
question and "what would change my mind" to `memory.md`. The **History** page shows every saved debate.

**Export:** "Download debate (.md)" saves the full transcript of every stage. Use these files for the
iteration log and the report.

**Languages:** 🇬🇧 English · 🇩🇪 Deutsch · 🇮🇹 Italiano · 🇫🇷 Français · 🇪🇸 Español. Both the interface and the model's answers switch.

---

## Project structure

```
app.py                 Streamlit interface: home → confirm → arena (+ History, How it works)
system.md              shared principles injected into every call
prompts/               one .md file per stage or role
skills/                extra guidance, loaded only when Stage 1 flags it
devil/
  llm.py               OpenAI-compatible client for Ollama, tolerant JSON parsing, <think> stripping
  pipeline.py          the stages and the Debate object (Judge blinding lives here)
  i18n.py              all UI text in 5 languages + examples + method page
  ui.py                theme (CSS) and HTML components: cards, pills, map, confidence gauge
  memory.py            memory.md / memory.json
  export.py            full debate → Markdown
  search.py            Tavily web search → numbered sources
  store.py             shared debate storage (Supabase or local file) + top-rated examples
supabase_schema.sql    the database table (run once in Supabase)
DEPLOY.md              step-by-step guide to the public link
tests/                 pipeline tests with a fake model (no Ollama needed): uv run pytest
.streamlit/config.toml dark theme
```

## Editing with OpenCode

Open this folder as the project in OpenCode and prompt it as in class (`AGENTS.md` gives it the context).
For example: *"Make the Devil cite a source for every 'supported' claim, using the Tavily tool"*, or
*"Add a Version selector (V1 baseline, V2 'act as devil's advocate', V3 single voice, V4) to the sidebar"*.
The app reloads automatically.

To change how an agent behaves, edit its `.md` file in `prompts/`. You don't need to touch any Python.

## Tests

```bash
uv run pytest -q
```
Checks the full pipeline, **that the Judge never sees the user's wording or confidence**, that skills load
only when flagged, tolerant JSON parsing, and the Markdown export.
