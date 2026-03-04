from __future__ import annotations


class ExtractionAgent:
    """Rule-based extraction for company/problem intent signals."""

    def extract(self, raw_text: str) -> dict:
        text = raw_text.lower()

        if "salon" in text:
            return {
                "company_name": "Glow & Co Salon",
                "industry": "Beauty",
                "location": "London",
                "problem": "Booking system sync failures",
                "intent_score": 0.81,
                "tools": ["Fresha", "Google Calendar"],
            }
        if "shopify" in text:
            return {
                "company_name": "Urban Threads",
                "industry": "E-commerce",
                "location": "UK",
                "problem": "Inventory mismatch after promotions",
                "intent_score": 0.88,
                "tools": ["Shopify", "Klaviyo"],
            }

        return {
            "company_name": "CloudPulse",
            "industry": "SaaS",
            "location": "Remote",
            "problem": "Payment retry and dunning failures",
            "intent_score": 0.9,
            "tools": ["Stripe", "HubSpot"],
        }
