from __future__ import annotations


class AlertAgent:
    def build_alert(self, opportunity_score: float, problem: str) -> tuple[str, str]:
        severity = "high" if opportunity_score >= 0.9 else "medium"
        alert_type = "opportunity_detected"
        message = f"{severity.upper()} signal: {problem}"
        return alert_type, message
