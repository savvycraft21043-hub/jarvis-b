from __future__ import annotations

from app.connectors.sources import SourceSignal, all_connectors


class DiscoveryAgent:
    """Collects real internet signals from public endpoints (HN, Reddit, RSS)."""

    def collect(self) -> tuple[list[dict], list[str]]:
        collected: list[dict] = []
        errors: list[str] = []

        for connector in all_connectors():
            try:
                for signal in connector.collect():
                    collected.append(self._to_dict(signal))
            except Exception as exc:
                errors.append(f"{connector.source_name}: {exc}")

        return collected, errors

    @staticmethod
    def _to_dict(signal: SourceSignal) -> dict:
        return {
            "source": signal.source,
            "source_url": signal.source_url,
            "content": signal.content,
            "captured_at": signal.captured_at,
            "metadata_json": signal.metadata_json,
        }
