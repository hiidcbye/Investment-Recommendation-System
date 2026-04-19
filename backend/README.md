# Backend - Investment Recommendation System

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install backend dependencies.

```bash
pip install -r requirements.txt
```

3. Copy .env.example to .env and configure DB credentials.

```bash
copy .env.example .env
```

4. Initialize and seed the database.

```bash
python init_db.py
```

## Running the Server

```bash
flask run
```

Runs on http://localhost:5000 by default.

## API Reference

| Method | Endpoint   | Description                     | Request Body / Params                   |
| ------ | ---------- | ------------------------------- | --------------------------------------- |
| GET    | /health    | Health check                    | None                                    |
| POST   | /recommend | Get investment recommendations  | {"risk": string, "budget": int}         |
| GET    | /history   | Get past recommendation history | ?limit=N (optional, default 10, max 50) |

## Module Overview

- app.py - Flask entry point and route definitions
- db.py - PostgreSQL connection factory
- config.py - loads environment variables
- data_processor.py - loads, cleans, filters, and ranks investment data
- recommender.py - orchestrates the recommendation pipeline
- history.py - saves and retrieves recommendation history
- init_db.py - initializes DB schema and seeds investment data
- schema.sql - table definitions
- seed.sql - sample investment data
