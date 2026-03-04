# JARVIS — Local AI-Powered Business Intelligence System

JARVIS is a local-first intelligence platform that ingests live public internet signals, extracts business pain points, scores opportunities, and presents findings in a modern dashboard.

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
│   │   ├── connectors/
│   │   │   └── sources.py
│   │   ├── core/
│   │   │   └── settings.py
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
│   │   │   ├── Sidebar.jsx
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
- **Real-source ingestion connectors:**
  - Hacker News API
  - Reddit public JSON feeds
  - RSS/Atom feeds (status + tech feeds)
- **Agents:**
  - `DiscoveryAgent`: collects public web signals from connectors
  - `ExtractionAgent`: infers company/problem/tool/intent
  - `OpportunityAgent`: computes opportunity score + summary
  - `QueryAgent`: full-text/natural query search
  - `AlertAgent`: creates alert severity + message
- **Pipeline service:** orchestrates all agents end-to-end (`/api/pipeline/run`)
- **Deduplication:** SHA256 content-hash to avoid duplicate raw signals

### Database schema

Tables:
- `raw_signals`
- `companies`
- `signals`
- `opportunities`
- `alerts`
- `ingestion_runs`

FTS:
- `signals_fts` virtual table for full-text search over signal/company/problem/content.

Schema is in `backend/app/db/schema.sql`.

## Frontend dashboard

- **Stack:** React + Vite + TailwindCSS
- **Design:** dark-mode default, card-based intelligence UI
- **Views:**
  1. Command Center (run ingestion + natural query)
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


## Merge conflict prevention

To reduce merge conflicts across VS Code/Windows/Linux collaborators:

- `.gitattributes` enforces stable line endings and a deterministic merge strategy for `frontend/package-lock.json`.
- `.gitignore` blocks local runtime files (`.venv`, `node_modules`, `dist`, `jarvis.db`, caches/logs) from being committed.

Recommended workflow before opening a PR:

```bash
git fetch origin
git rebase origin/main
# resolve any conflict locally if shown
git push --force-with-lease
```

## Windows PowerShell npm policy fix

If you get:
`npm.ps1 cannot be loaded because running scripts is disabled on this system`

Use one of the following:

```powershell
npm.cmd install
npm.cmd run dev
```

or set policy for current user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Test

```bash
cd backend
PYTHONPATH=. pytest -q
```

## Notes

- Uses only open-source libraries.
- Runs fully local (SQLite + local web servers).
- Ingestion is now live from public internet sources; results depend on available source data/network reachability.
