from app.db.database import init_db
from app.repositories import IntelligenceRepository
from app.services.pipeline import IntelligencePipeline


def test_pipeline_generates_records_with_mock_discovery(monkeypatch):
    init_db()
    repo = IntelligenceRepository()
    pipeline = IntelligencePipeline(repo)

    sample = [
        {
            "source": "reddit",
            "source_url": "https://example.com/1",
            "content": "Shopify merchants report inventory fail issue and need better tooling",
            "captured_at": "2026-01-01T00:00:00+00:00",
            "metadata_json": "{}",
        },
        {
            "source": "hackernews",
            "source_url": "https://example.com/2",
            "content": "Stripe billing error causing churn for SaaS teams",
            "captured_at": "2026-01-01T00:00:00+00:00",
            "metadata_json": "{}",
        },
    ]

    monkeypatch.setattr(pipeline.discovery, "collect", lambda: (sample, []))

    result = pipeline.run_once()

    assert result["discovered"] == 2
    assert result["raw_signals"] == 2
    assert len(repo.list_signals()) >= 2
    assert len(repo.list_opportunities()) >= 2


def test_pipeline_deduplicates_raw_signals(monkeypatch):
    init_db()
    repo = IntelligenceRepository()
    pipeline = IntelligencePipeline(repo)
    sample = [
        {
            "source": "reddit",
            "source_url": "https://example.com/dup",
            "content": "Shopify inventory mismatch fail",
            "captured_at": "2026-01-01T00:00:00+00:00",
            "metadata_json": "{}",
        }
    ]
    monkeypatch.setattr(pipeline.discovery, "collect", lambda: (sample, []))

    first = pipeline.run_once()
    second = pipeline.run_once()

    assert first["raw_signals"] == 1
    assert second["raw_signals"] == 0
