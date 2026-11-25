# Stage 5 — Reassess

The user has answered the Devil's questions. Show them what their reasoning looks like now.
Judge their answers on substance: a good answer can rescue part of the position; a vague
or evasive one leaves the gap open. Do not tell them what to believe.

Position (neutral restatement): "{{restatement}}"
Confidence before: {{confidence}}/100

Questions and the user's answers:
{{answers}}

Judge's map so far:
{{judge}}

Return JSON only:
{
  "survived": ["what held up, now including anything the answers rescued"],
  "needs_evidence": ["what still needs evidence"],
  "unexamined": ["assumptions still not examined"],
  "feedback": "2–3 sentences on how well the answers dealt with the gaps",
  "next_step": "one concrete thing the user could check or find out"
}

Write all text values in {{language}}.
