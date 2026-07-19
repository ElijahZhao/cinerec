"""
TMDB Metadata Enrichment — Fetch movie details from TMDB API.
Requires TMDB_API_KEY in .env file. Works without key (MovieLens-only data).
"""
import os, requests, json, time, pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Try to load .env
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
except ImportError:
    pass

TMDB_KEY = os.getenv("TMDB_API_KEY", "")

# MovieLens 100K item file columns
ITEM_FILE = os.path.join(RAW_DIR, "ml-100k", "u.item")
MOVIE_COLS = ["id", "title", "release_date", "video_date", "url",
              "unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
              "Crime", "Documentary", "Drama", "Fantasy", "Film_Noir", "Horror",
              "Musical", "Mystery", "Romance", "Sci_Fi", "Thriller", "War", "Western"]
GENRES = MOVIE_COLS[5:]
GENRE_NAMES = ["Action","Adventure","Animation","Children","Comedy","Crime",
               "Documentary","Drama","Fantasy","Film-Noir","Horror","Musical",
               "Mystery","Romance","Sci-Fi","Thriller","War","Western"]


def load_movielens_movies():
    """Load movie metadata from MovieLens u.item file."""
    if not os.path.exists(ITEM_FILE):
        print(f"Item file not found: {ITEM_FILE}")
        print("Generating minimal movie list from ratings.csv...")
        ratings_csv = os.path.join(RAW_DIR, "ratings.csv")
        if not os.path.exists(ratings_csv):
            raise FileNotFoundError("No data found. Run download.py first.")
        df = pd.read_csv(ratings_csv)
        movies = df[["item_id"]].drop_duplicates().sort_values("item_id")
        return pd.DataFrame({
            "id": movies["item_id"].values.astype(int),
            "title": [f"Movie {mid}" for mid in movies["item_id"].values],
            "genres": ["" for _ in range(len(movies))],
            "release_year": [None] * len(movies)
        })

    df = pd.read_csv(ITEM_FILE, sep="|", names=MOVIE_COLS, encoding="latin-1")
    genre_list = []
    for _, row in df.iterrows():
        g = [GENRE_NAMES[i] for i, col in enumerate(GENRES[1:]) if row[col] == 1]
        genre_list.append("|".join(g))
    df["genres"] = genre_list
    year = df["release_date"].str.extract(r"(\d{4})")[0]
    df["release_year"] = pd.to_numeric(year, errors="coerce").astype("Int64")
    return df[["id", "title", "genres", "release_year"]]


def search_tmdb(title, year=None):
    """Search TMDB for a movie by title and year."""
    if not TMDB_KEY:
        return None
    q = f"{title} ({int(year)})" if year and pd.notna(year) else title
    try:
        r = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"api_key": TMDB_KEY, "query": q, "page": 1},
            timeout=5
        )
        if r.status_code == 200:
            results = r.json().get("results", [])
            if results:
                return results[0]
    except Exception:
        pass
    return None


def enrich_all():
    """Enrich all MovieLens movies with TMDB metadata."""
    movies = load_movielens_movies()
    enriched = []
    found_count = 0

    for i, row in movies.iterrows():
        m = {
            "id": int(row["id"]),
            "title": row["title"],
            "genres": row["genres"],
            "release_year": None if pd.isna(row.get("release_year")) else int(row["release_year"]),
            "overview": "",
            "poster_url": "",
            "tmdb_id": ""
        }

        result = search_tmdb(row["title"], row.get("release_year"))
        if result:
            m["overview"] = result.get("overview", "")
            poster_path = result.get("poster_path", "")
            if poster_path:
                m["poster_url"] = f"https://image.tmdb.org/t/p/w342{poster_path}"
            m["tmdb_id"] = str(result.get("id", ""))
            release_date = result.get("release_date", "")
            if release_date and len(release_date) >= 4:
                m["release_year"] = int(release_date[:4])
            found_count += 1

        enriched.append(m)
        if (i + 1) % 100 == 0:
            print(f"Enriched {i + 1}/{len(movies)} movies ({found_count} found on TMDB)...")
            time.sleep(0.2)  # Rate limit

    out_path = os.path.join(PROCESSED_DIR, "movies_enriched.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)

    print(f"Done. {found_count}/{len(enriched)} movies found on TMDB.")
    print(f"Saved to {out_path}")


if __name__ == "__main__":
    if TMDB_KEY:
        print("TMDB API key found. Enriching with TMDB data...")
        enrich_all()
    else:
        print("No TMDB_API_KEY found. Creating enrichment from MovieLens-only data...")
        movies = load_movielens_movies()
        enriched = []
        for _, row in movies.iterrows():
            enriched.append({
                "id": int(row["id"]),
                "title": row["title"],
                "genres": row["genres"],
                "release_year": None if pd.isna(row.get("release_year")) else int(row["release_year"]),
                "overview": "",
                "poster_url": "",
                "tmdb_id": ""
            })
        out_path = os.path.join(PROCESSED_DIR, "movies_enriched.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(enriched, f, ensure_ascii=False, indent=2)
        print(f"Created {len(enriched)} entries from MovieLens-only data.")
        print(f"Saved to {out_path}")