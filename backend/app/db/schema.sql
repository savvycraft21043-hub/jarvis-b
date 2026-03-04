PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS raw_signals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  source_url TEXT,
  content TEXT NOT NULL,
  captured_at TEXT NOT NULL,
  metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS companies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  industry TEXT,
  location TEXT,
  website TEXT,
  tools_json TEXT,
  opportunity_score REAL DEFAULT 0,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS signals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  raw_signal_id INTEGER,
  company_id INTEGER,
  source TEXT NOT NULL,
  problem TEXT NOT NULL,
  intent_score REAL DEFAULT 0,
  signal_time TEXT NOT NULL,
  FOREIGN KEY(raw_signal_id) REFERENCES raw_signals(id) ON DELETE SET NULL,
  FOREIGN KEY(company_id) REFERENCES companies(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS opportunities (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  company_id INTEGER,
  industry TEXT NOT NULL,
  problem TEXT NOT NULL,
  opportunity_score REAL NOT NULL,
  summary TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(company_id) REFERENCES companies(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS alerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  opportunity_id INTEGER,
  alert_type TEXT NOT NULL,
  message TEXT NOT NULL,
  severity TEXT NOT NULL,
  created_at TEXT NOT NULL,
  is_read INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(opportunity_id) REFERENCES opportunities(id) ON DELETE CASCADE
);

CREATE VIRTUAL TABLE IF NOT EXISTS signals_fts USING fts5(
  company_name,
  source,
  problem,
  content,
  content=''
);
