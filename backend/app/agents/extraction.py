from __future__ import annotations

import re


class ExtractionAgent:
    """Rule + keyword extraction to infer company/problem/tool/intent from open-web signals."""

    INDUSTRY_KEYWORDS = {
        "E-commerce": ["shopify", "inventory", "checkout", "merchant", "cart"],
        "SaaS": ["saas", "billing", "api", "subscription", "churn", "dunning"],
        "Beauty": ["salon", "booking", "appointment", "spa"],
        "Fintech": ["payment", "stripe", "invoice", "payout", "refund"],
    }

    PROBLEM_PATTERNS = [
        (r"(outage|downtime|incident)", "Service reliability issues"),
        (r"(inventory|stock).*(wrong|mismatch|fail)", "Inventory synchronization failures"),
        (r"(billing|payment|dunning).*(fail|error|issue)", "Billing and payment recovery failures"),
        (r"(booking|appointment).*(fail|sync|double)", "Booking synchronization failures"),
        (r"(churn|cancel|refund)", "Revenue retention problems"),
    ]

    TOOL_KEYWORDS = [
        "Shopify",
        "Stripe",
        "HubSpot",
        "Salesforce",
        "Klaviyo",
        "Fresha",
        "Notion",
        "Intercom",
    ]

    COMPANY_HINTS = ["Shopify", "Stripe", "Square", "Toast", "Mindbody", "HubSpot", "Klaviyo"]

    def extract(self, raw_text: str) -> dict:
        text = raw_text.strip()
        lower = text.lower()

        industry = self._infer_industry(lower)
        problem = self._infer_problem(lower)
        tools = [tool for tool in self.TOOL_KEYWORDS if tool.lower() in lower]
        company_name = self._infer_company(text)
        location = self._infer_location(text)
        intent_score = self._intent_score(lower, problem, tools)

        return {
            "company_name": company_name,
            "industry": industry,
            "location": location,
            "problem": problem,
            "intent_score": intent_score,
            "tools": tools,
        }

    def _infer_industry(self, lower: str) -> str:
        for industry, keywords in self.INDUSTRY_KEYWORDS.items():
            if any(keyword in lower for keyword in keywords):
                return industry
        return "General Tech"

    def _infer_problem(self, lower: str) -> str:
        for pattern, label in self.PROBLEM_PATTERNS:
            if re.search(pattern, lower):
                return label
        return "Operational pain point detected"

    def _infer_company(self, text: str) -> str:
        for hint in self.COMPANY_HINTS:
            if hint.lower() in text.lower():
                return hint

        candidates = re.findall(r"\b[A-Z][a-zA-Z0-9&.-]{2,}\b", text)
        for token in candidates:
            if token.lower() not in {"the", "and", "for", "with", "from", "this", "that"}:
                return token
        return "Unknown Company"

    @staticmethod
    def _infer_location(text: str) -> str:
        known = ["London", "New York", "San Francisco", "Berlin", "Remote", "UK", "US"]
        for place in known:
            if place.lower() in text.lower():
                return place
        return "Unknown"

    @staticmethod
    def _intent_score(lower: str, problem: str, tools: list[str]) -> float:
        score = 0.45
        if "need" in lower or "looking for" in lower or "recommend" in lower:
            score += 0.2
        if "issue" in lower or "fail" in lower or "error" in lower or "outage" in lower:
            score += 0.2
        if problem != "Operational pain point detected":
            score += 0.1
        if tools:
            score += 0.05
        return round(min(score, 0.99), 2)
