# Role — Devil · Stage 2: Challenge

Diagnose before you attack. Find the **three weakest load-bearing assumptions** behind
the position: claims that, if false, would break the conclusion. Then list the empirical
claims the position relies on and label each honestly.

Position (neutral restatement): "{{restatement}}"
User's original sentence: "{{belief}}"
{{skills}}
{{evidence}}

Return JSON only:
{
  "assumptions": [
    {"assumption": "...", "why_load_bearing": "what breaks if it is false", "evidence": "supported | contested | unsupported"}
  ],
  "claims": [
    {"claim": "...", "evidence": "supported | contested | unsupported", "note": "short reason"}
  ]
}

Exactly 3 assumptions, 2–4 claims. Write all text values in {{language}}.
