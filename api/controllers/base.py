# ============================================================
#  Base Controller — DB connection helper
#  Author: Rodrigo Garcia Martinez (2309091)
# ============================================================

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """Return a PostgreSQL connection, or None if it fails."""
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", 5432),
            dbname=os.getenv("DB_NAME", "teamx_library"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            cursor_factory=RealDictCursor,
        )
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return None
