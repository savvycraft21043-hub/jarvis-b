from __future__ import annotations


class OpportunityAgent:
    def score(self, problem: str, intent_score: float) -> tuple[float, str]:
        urgency_boost = 0.12 if "fail" in problem.lower() else 0.06
        score = min(1.0, round(intent_score + urgency_boost, 2))
        summary = f"High-fit opportunity to solve: {problem.lower()}."
        return score, summary
