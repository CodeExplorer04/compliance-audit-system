import sqlite3

DB_NAME = "compliance.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS requirements(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        policy_id TEXT,
        requirement_id TEXT,
        requirement_text TEXT,
        evidence_source TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS evidence(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evidence_id TEXT,
        requirement_id TEXT,
        description TEXT,
        confidence_score REAL,
        verification_status TEXT,
        timestamp TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS mappings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        requirement_id TEXT,
        evidence_id TEXT,
        similarity_score REAL
    )
    """)

    conn.commit()
    conn.close()