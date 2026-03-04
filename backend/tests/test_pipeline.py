from app.db.database import init_db
from app.repositories import IntelligenceRepository
from app.services.pipeline import IntelligencePipeline


def test_pipeline_generates_records():
    init_db()
    repo = IntelligenceRepository()
    pipeline = IntelligencePipeline(repo)

    result = pipeline.run_once()

    assert result["raw_signals"] >= 3
    assert len(repo.list_signals()) >= 3
    assert len(repo.list_opportunities()) >= 3
