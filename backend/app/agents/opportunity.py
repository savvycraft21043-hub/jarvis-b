from __future__ import annotations


class OpportunityAgent:
    def score(self, problem: str, intent_score: float) -> tuple[float, str]:
        lower = problem.lower()
        severity = 0.0
        if "reliability" in lower or "failure" in lower:
            severity += 0.2
        if "payment" in lower or "billing" in lower:
            severity += 0.12
        if "inventory" in lower or "booking" in lower:
            severity += 0.1

        score = min(1.0, round(intent_score + severity, 2))
        summary = (
            f"Detected repeatable {problem.lower()} pattern with intent score {intent_score:.2f}; "
            "likely monetizable via workflow automation or tooling replacement."
        )
        return score, summary
