from __future__ import annotations

from app.agents.alert import AlertAgent
from app.agents.discovery import DiscoveryAgent
from app.agents.extraction import ExtractionAgent
from app.agents.opportunity import OpportunityAgent
from app.repositories import IntelligenceRepository


class IntelligencePipeline:
    def __init__(self, repository: IntelligenceRepository):
        self.repository = repository
        self.discovery = DiscoveryAgent()
        self.extraction = ExtractionAgent()
        self.opportunity = OpportunityAgent()
        self.alert = AlertAgent()

    def run_once(self) -> dict:
        run_id = self.repository.start_ingestion_run()
        discovered, discovery_errors = self.discovery.collect()
        created = {
            "run_id": run_id,
            "discovered": len(discovered),
            "raw_signals": 0,
            "signals": 0,
            "opportunities": 0,
            "alerts": 0,
            "errors": discovery_errors,
        }

        for raw in discovered:
            try:
                raw_id = self.repository.insert_raw_signal(raw)
                if raw_id is None:
                    continue
                created["raw_signals"] += 1

                entity = self.extraction.extract(raw["content"])
                score, summary = self.opportunity.score(entity["problem"], entity["intent_score"])
                company_id = self.repository.upsert_company(entity, score)
                self.repository.insert_signal(raw_id, company_id, raw["source"], entity["problem"], entity["intent_score"])
                created["signals"] += 1

                opportunity_id = self.repository.insert_opportunity(
                    company_id=company_id,
                    industry=entity["industry"],
                    problem=entity["problem"],
                    score=score,
                    summary=summary,
                )
                created["opportunities"] += 1

                alert_type, message = self.alert.build_alert(score, entity["problem"])
                self.repository.insert_alert(opportunity_id, alert_type, message, "high" if score >= 0.9 else "medium")
                created["alerts"] += 1
            except Exception as exc:
                created["errors"].append(str(exc))

        self.repository.finish_ingestion_run(
            run_id=run_id,
            discovered=created["discovered"],
            inserted=created["raw_signals"],
            errors=created["errors"],
        )
        return created
