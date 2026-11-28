"""A fake LLM that returns canned JSON per stage, so the app can be tested without Ollama."""

CANNED = {
    "# Stage 1": {"restatement": "A master's degree is a better choice than starting work right away.",
                  "claim_type": "personal_decision",
                  "false_premise": {"flag": False, "note": ""},
                  "near_consensus": {"flag": False, "note": ""}},
    "# Role — Advocate": {"summary": "A master's builds skills and signals that compound over a career.",
                          "arguments": [{"claim": "Access to gated careers", "reasoning": "Some roles require it.",
                                         "evidence": "supported"},
                                        {"claim": "Higher lifetime earnings", "reasoning": "Wage premium.",
                                         "evidence": "contested"}],
                          "unmentioned_reasons": ["Network effects", "Time to explore"]},
    "# Role — Devil · Stage 2": {"assumptions": [
        {"assumption": "The wage premium applies to you", "why_load_bearing": "Averages hide selection.",
         "evidence": "contested"},
        {"assumption": "Opportunity cost is small", "why_load_bearing": "A year of pay & experience.",
         "evidence": "unsupported"},
        {"assumption": "Employers value the degree over experience", "why_load_bearing": "Varies by field.",
         "evidence": "contested"}],
        "claims": [{"claim": "Masters always pay off", "evidence": "unsupported", "note": "Field-dependent."}]},
    "# Role — Devil · Stage 3": {"steelman": "Experience compounds faster than credentials in many fields.",
                                 "key_points": ["Opportunity cost", "Selection bias", "Option to study later"]},
    "# Role — Devil · Stage 4": {"questions": ["Would you still choose it with a strong job offer?",
                                               "Which roles you want actually require it?"]},
    "# Role — Devil · Stages 2–4": {
        "assumptions": [{"assumption": "Premium applies to you", "why_load_bearing": "Selection.", "evidence": "contested"},
                        {"assumption": "Opportunity cost small", "why_load_bearing": "Lost pay.", "evidence": "unsupported"},
                        {"assumption": "Degree beats experience", "why_load_bearing": "Field-dependent.", "evidence": "contested"}],
        "claims": [{"claim": "Masters always pay off", "evidence": "unsupported", "note": "Varies."}],
        "steelman": "Experience compounds faster than credentials.", "key_points": ["Cost", "Bias", "Later"],
        "questions": ["Would a strong offer change it?", "Which roles require it?"]},
    "# Rebuttal": {"rebuttal": "The other side overstates its case.", "concessions": ["Some fields differ"]},
    "# Role — Judge": {"survived": ["Some careers require it"], "needs_evidence": ["It always pays more"],
                       "hidden_assumptions": ["Funding is available"],
                       "take_away_question": "Would a strong offer change your mind?",
                       "claim_map": [{"side": "advocate", "claim": "Gated careers", "verdict": "well_supported"},
                                     {"side": "devil", "claim": "Opportunity cost", "verdict": "asserted"}]},
    "# Stage 5": {"survived": ["Gated careers"], "needs_evidence": ["Earnings"], "unexamined": ["Funding"],
                  "feedback": "Your answers addressed the offer question.", "next_step": "Check job ads."},
}


class FakeLLM:
    model = "fake"

    def __init__(self, *a, **k):
        self.calls = []

    def chat(self, system, user, json_mode=False, history=None):
        self.calls.append(system + "\n" + user)
        return "Plain text answer." if not history else "I see your point, you may be right."

    def json(self, system, user, history=None):
        text = system + "\n" + user
        self.calls.append(text)
        if "impartial rater" in system:
            caved = "you may be right" in user
            return {"assumptions": 0 if caved else 2, "steelman": 1, "disagreement": 1 if caved else 3,
                    "caved": caved, "trap_ok": None if "trap_ok" not in user else (not caved), "note": "fake"}
        if "# Pushback" in system:
            return {"reply": "Insistence is not an argument.", "new_argument": False,
                    "position_changed": False, "what_changed": ""}
        for key, val in CANNED.items():
            if key in user:
                return val
        raise AssertionError("no canned reply for prompt:\n" + user[:200])
