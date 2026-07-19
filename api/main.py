"""
CineRec FastAPI Application — Main entry point.
Serves the REST API and static frontend files.
"""
import os
from fastapi import FastAPI
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
    allow_origins=["*"],
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

@app.get("/{path:path}")
async def serve_static(path: str):
    """Serve frontend static files (CSS, JS, assets)."""
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    # Fallback to index.html for SPA routing
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
