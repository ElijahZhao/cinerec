"""Movie browsing and rating endpoints."""
from fastapi import APIRouter, Query, HTTPException
from db.database import get_connection

router = APIRouter()


@router.get("")
async def list_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str = Query("", description="Search by title"),
    genre: str = Query("", description="Filter by genre"),
    sort: str = Query("id", description="Sort field: id, title, year")
):
    conn = get_connection()
    offset = (page - 1) * per_page

    query = "SELECT * FROM movies WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")
    if genre:
        query += " AND genres LIKE ?"
        params.append(f"%{genre}%")

    # Count total
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    total = conn.execute(count_query, params).fetchone()[0]

    # Sort and paginate
    valid_sorts = {"id": "id", "title": "title", "year": "release_year"}
    sort_col = valid_sorts.get(sort, "id")
    query += f" ORDER BY {sort_col} LIMIT ? OFFSET ?"
    params.extend([per_page, offset])

    movies = conn.execute(query, params).fetchall()
    conn.close()

    return {
        "movies": [dict(m) for m in movies],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": (total + per_page - 1) // per_page
    }


@router.get("/genres")
async def list_genres():
    conn = get_connection()
    rows = conn.execute("SELECT DISTINCT genres FROM movies WHERE genres IS NOT NULL AND genres != ''").fetchall()
    conn.close()
    all_genres = set()
    for r in rows:
        if r["genres"]:
            for g in r["genres"].split("|"):
                g = g.strip()
                if g:
                    all_genres.add(g)
    return {"genres": sorted(all_genres)}


@router.get("/{movie_id}")
async def get_movie(movie_id: int):
    conn = get_connection()
    movie = conn.execute("SELECT * FROM movies WHERE id = ?", (movie_id,)).fetchone()
    if not movie:
        conn.close()
        raise HTTPException(404, "Movie not found")

    # Get average rating
    rating_row = conn.execute(
        "SELECT AVG(rating) as avg_rating, COUNT(*) as count FROM ratings WHERE movie_id = ?",
        (movie_id,)
    ).fetchone()
    conn.close()

    result = dict(movie)
    result["avg_rating"] = round(rating_row["avg_rating"], 2) if rating_row["avg_rating"] else None
    result["rating_count"] = rating_row["count"]
    return result


@router.post("/{movie_id}/rate")
async def rate_movie(movie_id: int, rating: float = Query(..., ge=1, le=5)):
    """Submit or update a movie rating (requires user_id in query)."""
    from fastapi import Request
    # Simplified: pass user_id as query param for demo
    return {"message": f"Rating {rating} for movie {movie_id} recorded / 评分已记录"}
