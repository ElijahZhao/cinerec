"""
CineRec FastAPI Application — Main entry point.
Serves the REST API and static frontend files.
"""
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="CineRec — Multi-Modal Movie Recommendation System",
    description="A 5-level algorithm recommendation system with explainability",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from api.auth import router as auth_router
from api.movies import router as movies_router
from api.recommend import router as recommend_router
from api.eval_api import router as eval_router

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(movies_router, prefix="/api/movies", tags=["Movies"])
app.include_router(recommend_router, prefix="/api/recommend", tags=["Recommendations"])
app.include_router(eval_router, prefix="/api/eval", tags=["Evaluation"])

# Serve frontend static files
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/static/{path:path}")
async def serve_static(path: str):
    """Serve frontend static files (CSS, JS, assets)."""
    file_path = os.path.normpath(os.path.join(FRONTEND_DIR, path))
    # 防止路径遍历
    if not file_path.startswith(os.path.normpath(FRONTEND_DIR)):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Not Found")
    return FileResponse(file_path)
