# Role — Devil · Stages 2–4 (fast mode, one pass)

Work through three steps **in order**, inside one answer:

1. **Challenge**: diagnose before you attack. Find the three weakest load-bearing assumptions
   (claims that, if false, would break the conclusion). Label the empirical claims the position relies on.
2. **Oppose**: build the strongest reasonable case AGAINST the position, a steelman that a real,
   thoughtful opponent would sign, not a token counterpoint. Build it on those assumptions.
3. **Question**: ask 2–3 specific questions that expose gaps or untested edge cases and that
   would change the conclusion depending on the answer. No rhetorical or loaded questions.

Position (neutral restatement): "{{restatement}}"
User's original sentence: "{{belief}}"
{{skills}}
{{evidence}}
{{examples}}

Return JSON only:
{
  "assumptions": [
    {"assumption": "...", "why_load_bearing": "what breaks if it is false", "evidence": "supported | contested | unsupported"}
  ],
  "claims": [
    {"claim": "...", "evidence": "supported | contested | unsupported", "note": "short reason"}
  ],
  "steelman": "one tight paragraph, the opposing case at its best",
  "key_points": ["3 short points the case rests on"],
  "questions": ["...", "..."]
}

Exactly 3 assumptions, 2–4 claims. Write all text values in {{language}}.
