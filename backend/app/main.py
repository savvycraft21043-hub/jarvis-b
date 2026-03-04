from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.agents.query import QueryAgent
from app.db.database import init_db
from app.repositories import IntelligenceRepository
from app.services.pipeline import IntelligencePipeline

app = FastAPI(title="JARVIS Intelligence Engine", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repository = IntelligenceRepository()
pipeline = IntelligencePipeline(repository)
query_agent = QueryAgent(repository)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/pipeline/run")
def run_pipeline() -> dict:
    return pipeline.run_once()


@app.get("/api/search")
def search(q: str = Query(..., min_length=2)) -> dict:
    return query_agent.run(q)


@app.get("/api/opportunities")
def opportunities() -> list[dict]:
    return repository.list_opportunities()


@app.get("/api/signals")
def signals() -> list[dict]:
    return repository.list_signals()


@app.get("/api/companies")
def companies() -> list[dict]:
    return repository.list_companies()


@app.get("/api/companies/{company_id}")
def company_detail(company_id: int) -> dict:
    data = repository.get_company(company_id)
    if not data:
        raise HTTPException(status_code=404, detail="Company not found")
    return data


@app.get("/api/graph")
def graph() -> dict:
    return repository.graph()
