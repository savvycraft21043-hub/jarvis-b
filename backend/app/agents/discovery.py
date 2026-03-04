from __future__ import annotations

from datetime import datetime, timezone


class DiscoveryAgent:
    """Seed-like discovery agent that simulates internet crawl signals."""

    def collect(self) -> list[dict]:
        now = datetime.now(timezone.utc).isoformat()
        return [
            {
                "source": "reddit",
                "source_url": "https://reddit.com/r/smallbusiness",
                "content": "Our London salon keeps missing appointments because bookings sync fails.",
                "captured_at": now,
                "metadata_json": '{"subreddit":"smallbusiness"}',
            },
            {
                "source": "x",
                "source_url": "https://x.com/example/status/1",
                "content": "Shopify inventory is wrong after every flash sale. Need a reliable sync tool.",
                "captured_at": now,
                "metadata_json": '{"lang":"en"}',
            },
            {
                "source": "g2-review",
                "source_url": "https://g2.com/products/payment/reviews",
                "content": "Our SaaS billing retries fail and churn is climbing due to payment dunning gaps.",
                "captured_at": now,
                "metadata_json": '{"rating":2}',
            },
        ]
