# Grocery List Keeper

A simple Flask and SQLite grocery list application for local development and blue-green deployment practice.

## Run locally

```bash
cd "/Users/pankaj/Terraform Mini Project 4/App"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000.

## Environment variables

```bash
export APP_VERSION=v1.0.0
export APP_ENVIRONMENT=development
export PORT=5000
```

## Health check

```bash
curl http://localhost:5000/health
```

SQLite creates `grocery.db` automatically on first startup.
