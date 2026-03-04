from __future__ import annotations

from app.repositories import IntelligenceRepository


class QueryAgent:
    def __init__(self, repository: IntelligenceRepository):
        self.repository = repository

    def run(self, query: str) -> dict:
        return self.repository.search(query)
