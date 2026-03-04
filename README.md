# JARVIS — Local AI-Powered Business Intelligence System

JARVIS is a local-first intelligence platform that discovers problem signals from internet-like sources, extracts business pain points, scores opportunities, and presents findings in a modern dashboard.

## Project structure

```text
jarvis-b/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── alert.py
│   │   │   ├── discovery.py
│   │   │   ├── extraction.py
│   │   │   ├── opportunity.py
│   │   │   └── query.py
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── schema.sql
│   │   ├── services/
│   │   │   └── pipeline.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── repositories.py
│   ├── requirements.txt
│   └── tests/
│       └── test_pipeline.py
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Sidebar.jsx
│   │   │   └── ui.jsx
    │   ├── lib/
    │   │   └── api.js
    │   ├── pages/
    │   │   ├── CommandCenter.jsx
    │   │   ├── CompanyPage.jsx
    │   │   ├── GraphView.jsx
    │   │   ├── OpportunityRadar.jsx
    │   │   └── SignalFeed.jsx
    │   ├── App.jsx
    │   ├── index.css
    │   └── main.jsx
    ├── package.json
    ├── postcss.config.js
    ├── tailwind.config.js
    └── vite.config.js
```

## Backend intelligence engine

- **Framework:** FastAPI
- **Database:** SQLite + FTS5
- **Agents:**
  - `DiscoveryAgent`: collects raw internet-like signals
  - `ExtractionAgent`: extracts company/problem/tool/intent
  - `OpportunityAgent`: computes opportunity score and summary
  - `QueryAgent`: handles natural-language-like search
  - `AlertAgent`: creates alert messages and severity
- **Pipeline service:** orchestrates all agents end-to-end (`/api/pipeline/run`)

### Database schema

Tables:
- `raw_signals`
- `companies`
- `signals`
- `opportunities`
- `alerts`

FTS:
- `signals_fts` virtual table for full-text query over signal/company/problem/content.

Schema is in `backend/app/db/schema.sql`.

## Frontend dashboard

- **Stack:** React + Vite + TailwindCSS
- **Design:** dark-mode default, card-based minimal intelligence UI
- **Views:**
  1. Command Center (global natural query input)
  2. Opportunity Radar
  3. Signal Feed
  4. Company Intelligence page
  5. Graph View (company/tool/opportunity relationships)

## API endpoints

- `GET /health`
- `POST /api/pipeline/run`
- `GET /api/search?q=...`
- `GET /api/opportunities`
- `GET /api/signals`
- `GET /api/companies`
- `GET /api/companies/{id}`
- `GET /api/graph`

## Run locally

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Test

```bash
cd backend
PYTHONPATH=. pytest -q
```

## Notes

- Uses only open-source libraries.
- Runs fully local (SQLite + local web server).
- Current signal discovery is mock/seeded for deterministic local demos and easy extension.
