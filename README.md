# Grocery List Keeper

A simple Flask and SQLite grocery list application for local development and blue-green deployment practice.

## Run locally

```bash
cd "Grocery List Keeper/App"
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

## Azure App Service deployment

Configure the Web App with these values before running Deployment Center:

- **Stack:** Python
- **Python version:** 3.11 or another supported Python 3 version
- **Startup command:** `gunicorn --bind=0.0.0.0:$PORT --timeout 600 app:app`
- **Application root:** leave empty when this repository is connected directly; the repository root contains `app.py` and `requirements.txt`

The Web App must not be configured as PHP. Oryx detects Python from `requirements.txt`; a PHP stack forces Oryx to search for PHP files and produces a platform detection error.