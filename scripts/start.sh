#!/bin/bash
# CineRec — Local Development Quick Start
# Usage: bash scripts/start.sh

set -e
cd "$(dirname "$0")/.."

echo "=== CineRec — Starting Development Server ==="

# Check if data exists
if [ ! -f "data/raw/ratings.csv" ]; then
    echo "[1/3] Downloading MovieLens 100K..."
    python data/download.py
else
    echo "[1/3] Data already exists, skipping download."
fi

# Check if database exists
if [ ! -f "db/cinerec.db" ]; then
    echo "[2/3] Initializing database..."
    python -c "from db.init_db import init_db; import os; init_db(os.path.join('data','raw','ratings.csv'))"
else
    echo "[2/3] Database already exists, skipping init."
fi

# Start server
echo "[3/3] Starting FastAPI server..."
echo ""
echo "CineRec is running at: http://localhost:8000"
echo "Press Ctrl+C to stop."
echo ""
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
