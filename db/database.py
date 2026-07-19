import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "cinerec.db")

def get_connection():
    """Get a SQLite connection with Row factory for dict-like access."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """Run one-time schema initialisations (idempotent)."""
    conn = get_connection()
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_ratings_user_movie ON ratings(user_id, movie_id)")
    conn.commit()
    conn.close()


class DBConnection:
    """Context manager for database connections with auto commit/rollback."""

    def __enter__(self):
        self.conn = get_connection()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        return False