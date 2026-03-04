from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

import feedparser
import requests

from app.core.settings import settings


@dataclass
class SourceSignal:
    source: str
    source_url: str
    content: str
    captured_at: str
    metadata_json: str


class SourceConnector:
    source_name: str

    def collect(self) -> Iterable[SourceSignal]:
        raise NotImplementedError


class HNConnector(SourceConnector):
    source_name = "hackernews"

    def collect(self) -> Iterable[SourceSignal]:
        top_ids_resp = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=settings.request_timeout_seconds,
            headers={"User-Agent": settings.user_agent},
        )
        top_ids_resp.raise_for_status()
        story_ids = top_ids_resp.json()[: settings.max_items_per_source]

        for story_id in story_ids:
            story_resp = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                timeout=settings.request_timeout_seconds,
                headers={"User-Agent": settings.user_agent},
            )
            story_resp.raise_for_status()
            story = story_resp.json() or {}
            title = story.get("title")
            if not title:
                continue

            text = story.get("text", "")
            content = f"{title}. {text}".strip()
            source_url = story.get("url") or f"https://news.ycombinator.com/item?id={story_id}"
            captured = datetime.now(timezone.utc).isoformat()
            yield SourceSignal(
                source=self.source_name,
                source_url=source_url,
                content=content,
                captured_at=captured,
                metadata_json=f'{{"hn_id": {story_id}}}',
            )


class RedditConnector(SourceConnector):
    source_name = "reddit"

    SUBREDDITS = ["shopify", "smallbusiness", "saas", "entrepreneur"]

    def collect(self) -> Iterable[SourceSignal]:
        for subreddit in self.SUBREDDITS:
            resp = requests.get(
                f"https://www.reddit.com/r/{subreddit}/new.json?limit={settings.max_items_per_source}",
                timeout=settings.request_timeout_seconds,
                headers={"User-Agent": settings.user_agent},
            )
            resp.raise_for_status()
            payload = resp.json()
            children = payload.get("data", {}).get("children", [])

            for child in children:
                data = child.get("data", {})
                title = data.get("title", "")
                body = data.get("selftext", "")
                if not title:
                    continue

                permalink = data.get("permalink", "")
                source_url = f"https://www.reddit.com{permalink}" if permalink else "https://www.reddit.com"
                content = f"{title}. {body}".strip()
                captured = datetime.now(timezone.utc).isoformat()
                yield SourceSignal(
                    source=self.source_name,
                    source_url=source_url,
                    content=content,
                    captured_at=captured,
                    metadata_json=f'{{"subreddit":"{subreddit}"}}',
                )


class RSSConnector(SourceConnector):
    source_name = "rss"

    FEEDS = [
        "https://status.shopify.com/history.atom",
        "https://status.stripe.com/history.atom",
        "https://news.ycombinator.com/rss",
    ]

    def collect(self) -> Iterable[SourceSignal]:
        for feed in self.FEEDS:
            parsed = feedparser.parse(feed)
            entries = parsed.entries[: settings.max_items_per_source]
            for entry in entries:
                title = getattr(entry, "title", "")
                summary = getattr(entry, "summary", "")
                if not title:
                    continue
                captured = datetime.now(timezone.utc).isoformat()
                source_url = getattr(entry, "link", feed)
                content = f"{title}. {summary}".strip()
                yield SourceSignal(
                    source=self.source_name,
                    source_url=source_url,
                    content=content,
                    captured_at=captured,
                    metadata_json=f'{{"feed":"{feed}"}}',
                )


def all_connectors() -> list[SourceConnector]:
    return [HNConnector(), RedditConnector(), RSSConnector()]
