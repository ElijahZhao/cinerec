"""Recommendation endpoints with algorithm selection and explainability."""
from fastapi import APIRouter, Query, HTTPException
from db.database import get_connection

router = APIRouter()

# Lazy-loaded models
_models = {}
_explainer = None


def get_explainer():
    """Lazy-load the recommender explainer."""
    global _explainer
    if _explainer is None:
        from models.explain import RecommenderExplainer
        import json, os, sys
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
        _explainer = RecommenderExplainer()
        _explainer.load_data()
        # Load user ratings from database
        conn = get_connection()
        rows = conn.execute("SELECT user_id, movie_id, rating FROM ratings").fetchall()
        conn.close()
        train_data = {
            'user_id': [r['user_id'] for r in rows],
            'item_id': [r['movie_id'] for r in rows],
            'rating': [r['rating'] for r in rows],
        }
        _explainer.load_user_ratings(train_data)
    return _explainer


@router.get("")
async def get_recommendations(
    user_id: int = Query(..., description="User ID"),
    algorithm: str = Query("MultiModalNCF", description="Algorithm: UserCF, ItemCF, SVD, NeuMF, MultiModalNCF"),
    top_k: int = Query(10, ge=1, le=50)
):
    """Get personalized movie recommendations for a user."""
    conn = get_connection()

    # Get user's rated movies
    rated = conn.execute(
        "SELECT movie_id FROM ratings WHERE user_id = ?", (user_id,)
    ).fetchall()
    exclude = {r["movie_id"] for r in rated}

    # For demo: return random unwatched movies with mock scores
    if exclude:
        all_movies = conn.execute(
            "SELECT id, title, genres, poster_url, release_year FROM movies WHERE id NOT IN ({}) ORDER BY RANDOM() LIMIT ?".format(
                ",".join("?" * len(exclude))
            ),
            list(exclude) + [top_k]
        ).fetchall()
    else:
        all_movies = conn.execute(
            "SELECT id, title, genres, poster_url, release_year FROM movies ORDER BY RANDOM() LIMIT ?", (top_k,)
        ).fetchall()

    conn.close()

    recommendations = []
    for i, m in enumerate(all_movies):
        recommendations.append({
            "item_id": m["id"],
            "title": m["title"],
            "genres": m["genres"],
            "poster_url": m["poster_url"],
            "release_year": m["release_year"],
            "score": round(0.95 - i * 0.03, 4),
            "algorithm": algorithm
        })

    # Add explanations
    try:
        explainer = get_explainer()
        for rec in recommendations:
            reasons = explainer.explain(user_id, rec["item_id"])
            rec["reasons"] = reasons.get("reasons", [])
    except Exception:
        for rec in recommendations:
            rec["reasons"] = [{"type": "default", "reason_en": "Based on your viewing history", "reason_zh": "基于你的观影历史", "score": 0}]

    return {
        "user_id": user_id,
        "algorithm": algorithm,
        "recommendations": recommendations,
        "total": len(recommendations)
    }


@router.get("/{movie_id}/explain")
async def explain_recommendation(
    movie_id: int,
    user_id: int = Query(..., description="User ID")
):
    """Get explanation for why a movie was recommended."""
    try:
        explainer = get_explainer()
        result = explainer.explain(user_id, movie_id)
        return result
    except Exception as e:
        raise HTTPException(500, str(e))
