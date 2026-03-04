from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from app.db.database import db_session


class IntelligenceRepository:
    def start_ingestion_run(self) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with db_session() as conn:
            cur = conn.execute("INSERT INTO ingestion_runs(started_at) VALUES (?)", (now,))
            return int(cur.lastrowid)

    def finish_ingestion_run(self, run_id: int, discovered: int, inserted: int, errors: list[str]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with db_session() as conn:
            conn.execute(
                """
                UPDATE ingestion_runs
                SET finished_at=?, discovered_count=?, inserted_count=?, errors_json=?
                WHERE id=?
                """,
                (now, discovered, inserted, json.dumps(errors), run_id),
            )

    def insert_raw_signal(self, signal: dict) -> int | None:
        content_hash = hashlib.sha256(
            f"{signal.get('source','')}|{signal.get('source_url','')}|{signal.get('content','')}".encode("utf-8")
        ).hexdigest()
        with db_session() as conn:
            existing = conn.execute("SELECT id FROM raw_signals WHERE content_hash = ?", (content_hash,)).fetchone()
            if existing:
                return None

            cur = conn.execute(
                """
                INSERT INTO raw_signals(source, source_url, content, content_hash, captured_at, metadata_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    signal["source"],
                    signal.get("source_url"),
                    signal["content"],
                    content_hash,
                    signal["captured_at"],
                    signal.get("metadata_json"),
                ),
            )
            return int(cur.lastrowid)

    def upsert_company(self, entity: dict, opportunity_score: float) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with db_session() as conn:
            cur = conn.execute("SELECT id FROM companies WHERE name = ?", (entity["company_name"],))
            row = cur.fetchone()
            tools_json = json.dumps(entity.get("tools", []))
            if row:
                conn.execute(
                    """
                    UPDATE companies
                    SET industry=?, location=?, tools_json=?, opportunity_score=?
                    WHERE id=?
                    """,
                    (
                        entity.get("industry"),
                        entity.get("location"),
                        tools_json,
                        opportunity_score,
                        row["id"],
                    ),
                )
                return int(row["id"])

            cur = conn.execute(
                """
                INSERT INTO companies(name, industry, location, website, tools_json, opportunity_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entity["company_name"],
                    entity.get("industry"),
                    entity.get("location"),
                    None,
                    tools_json,
                    opportunity_score,
                    now,
                ),
            )
            return int(cur.lastrowid)

    def insert_signal(self, raw_signal_id: int, company_id: int, source: str, problem: str, intent_score: float) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with db_session() as conn:
            cur = conn.execute(
                """
                INSERT INTO signals(raw_signal_id, company_id, source, problem, intent_score, signal_time)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (raw_signal_id, company_id, source, problem, intent_score, now),
            )
            signal_id = int(cur.lastrowid)
            company = conn.execute("SELECT name FROM companies WHERE id=?", (company_id,)).fetchone()
            content = conn.execute("SELECT content FROM raw_signals WHERE id=?", (raw_signal_id,)).fetchone()
            conn.execute(
                "INSERT INTO signals_fts(rowid, company_name, source, problem, content) VALUES (?, ?, ?, ?, ?)",
                (
                    signal_id,
                    company["name"] if company else "",
                    source,
                    problem,
                    content["content"] if content else "",
                ),
            )
            return signal_id

    def insert_opportunity(self, company_id: int, industry: str, problem: str, score: float, summary: str) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with db_session() as conn:
            cur = conn.execute(
                """
                INSERT INTO opportunities(company_id, industry, problem, opportunity_score, summary, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (company_id, industry, problem, score, summary, now),
            )
            return int(cur.lastrowid)

    def insert_alert(self, opportunity_id: int, alert_type: str, message: str, severity: str) -> int:
        now = datetime.now(timezone.utc).isoformat()
        with db_session() as conn:
            cur = conn.execute(
                """
                INSERT INTO alerts(opportunity_id, alert_type, message, severity, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (opportunity_id, alert_type, message, severity, now),
            )
            return int(cur.lastrowid)

    def list_signals(self, limit: int = 50) -> list[dict]:
        with db_session() as conn:
            rows = conn.execute(
                """
                SELECT s.id, s.source, s.problem, s.intent_score, s.signal_time, c.name AS company_name
                FROM signals s
                LEFT JOIN companies c ON c.id = s.company_id
                ORDER BY s.signal_time DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]

    def list_opportunities(self, limit: int = 50) -> list[dict]:
        with db_session() as conn:
            rows = conn.execute(
                """
                SELECT o.id, o.industry, o.problem, o.opportunity_score, o.summary, o.created_at, c.name AS company_name
                FROM opportunities o
                LEFT JOIN companies c ON c.id = o.company_id
                ORDER BY o.opportunity_score DESC, o.created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]

    def list_companies(self) -> list[dict]:
        with db_session() as conn:
            rows = conn.execute("SELECT * FROM companies ORDER BY opportunity_score DESC").fetchall()
            companies = []
            for row in rows:
                record = dict(row)
                record["tools"] = json.loads(record["tools_json"] or "[]")
                companies.append(record)
            return companies

    def get_company(self, company_id: int) -> dict | None:
        with db_session() as conn:
            row = conn.execute("SELECT * FROM companies WHERE id=?", (company_id,)).fetchone()
            if not row:
                return None
            company = dict(row)
            company["tools"] = json.loads(company["tools_json"] or "[]")
            signals = conn.execute(
                "SELECT id, source, problem, intent_score, signal_time FROM signals WHERE company_id=? ORDER BY signal_time DESC",
                (company_id,),
            ).fetchall()
            opps = conn.execute(
                "SELECT id, industry, problem, opportunity_score, summary, created_at FROM opportunities WHERE company_id=? ORDER BY created_at DESC",
                (company_id,),
            ).fetchall()
            company["signals"] = [dict(s) for s in signals]
            company["opportunities"] = [dict(o) for o in opps]
            return company

    def graph(self) -> dict:
        with db_session() as conn:
            rows = conn.execute(
                """
                SELECT c.id AS company_id, c.name AS company_name, c.industry, c.tools_json,
                       o.id AS opportunity_id, o.problem
                FROM companies c
                LEFT JOIN opportunities o ON o.company_id = c.id
                """
            ).fetchall()
        nodes = {}
        edges = []
        for row in rows:
            company_node_id = f"company:{row['company_id']}"
            nodes[company_node_id] = {"id": company_node_id, "label": row["company_name"], "group": "company"}
            if row["industry"]:
                ind_id = f"industry:{row['industry']}"
                nodes[ind_id] = {"id": ind_id, "label": row["industry"], "group": "industry"}
                edges.append({"source": company_node_id, "target": ind_id, "relation": "operates_in"})
            for tool in json.loads(row["tools_json"] or "[]"):
                tool_id = f"tool:{tool}"
                nodes[tool_id] = {"id": tool_id, "label": tool, "group": "tool"}
                edges.append({"source": company_node_id, "target": tool_id, "relation": "uses"})
            if row["opportunity_id"]:
                opp_id = f"opportunity:{row['opportunity_id']}"
                nodes[opp_id] = {"id": opp_id, "label": row["problem"], "group": "opportunity"}
                edges.append({"source": company_node_id, "target": opp_id, "relation": "has_opportunity"})

        return {"nodes": list(nodes.values()), "edges": edges}

    def search(self, query: str) -> dict:
        with db_session() as conn:
            signals = conn.execute(
                """
                SELECT s.id, s.source, s.problem, s.intent_score, s.signal_time, c.name AS company_name
                FROM signals_fts f
                JOIN signals s ON s.id = f.rowid
                LEFT JOIN companies c ON c.id = s.company_id
                WHERE signals_fts MATCH ?
                ORDER BY rank
                LIMIT 20
                """,
                (query,),
            ).fetchall()
            companies = conn.execute(
                "SELECT id, name, industry, location, opportunity_score FROM companies WHERE name LIKE ? OR industry LIKE ? LIMIT 20",
                (f"%{query}%", f"%{query}%"),
            ).fetchall()
            opportunities = conn.execute(
                "SELECT o.id, o.industry, o.problem, o.opportunity_score, c.name AS company_name FROM opportunities o LEFT JOIN companies c ON c.id=o.company_id WHERE o.problem LIKE ? LIMIT 20",
                (f"%{query}%",),
            ).fetchall()
        return {
            "query": query,
            "signals": [dict(s) for s in signals],
            "companies": [dict(c) for c in companies],
            "opportunities": [dict(o) for o in opportunities],
        }
