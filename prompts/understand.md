# Stage 1 — Understand

Restate the user's belief in neutral terms, with **no evaluation**. Keep their meaning
exactly; strip emotional or conviction language ("I'm absolutely sure", "obviously").
The restatement is the only version of the belief the Judge will ever see, so it must be
fair and complete.

Also classify the belief and run two quick checks:
- `false_premise`: is the statement built on a factually wrong premise (e.g. a well-known
  myth)? Only flag clear cases.
- `near_consensus`: is the core claim a near-consensus fact among experts (e.g. smoking
  raises lung-cancer risk)?

User's belief: "{{belief}}"

Return JSON only:
{
  "restatement": "one or two neutral sentences",
  "claim_type": "personal_decision | empirical | value | policy | mixed",
  "false_premise": {"flag": false, "note": "which premise is wrong and why, or empty"},
  "near_consensus": {"flag": false, "note": "why, or empty"},
  "search_queries": ["a neutral web query for evidence FOR the claim", "a neutral web query for evidence AGAINST it", "a query for the most relevant data or studies"]
}

Write the search_queries in English (better search results).

Write all text values in {{language}}.
