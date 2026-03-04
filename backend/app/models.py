from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Signal(BaseModel):
    id: int
    source: str
    problem: str
    company_name: str | None = None
    intent_score: float
    signal_time: str


class Opportunity(BaseModel):
    id: int
    company_name: str | None = None
    industry: str
    problem: str
    opportunity_score: float
    summary: str | None = None
    created_at: str


class CompanyDetail(BaseModel):
    id: int
    name: str
    industry: str | None = None
    location: str | None = None
    website: str | None = None
    tools: list[str] = []
    opportunity_score: float
    signals: list[Signal] = []
    opportunities: list[Opportunity] = []


class GraphNode(BaseModel):
    id: str
    label: str
    group: str


class GraphEdge(BaseModel):
    source: str
    target: str
    relation: str


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class SearchResponse(BaseModel):
    query: str
    companies: list[dict[str, Any]]
    signals: list[dict[str, Any]]
    opportunities: list[dict[str, Any]]
