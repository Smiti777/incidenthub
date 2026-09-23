import sqlite3

DATABASE = "incidenthub.db"


def init_db():
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            service TEXT NOT NULL,
            severity TEXT NOT NULL,
            description TEXT NOT NULL,
            assigned_to TEXT,
            status TEXT NOT NULL DEFAULT 'Open',
            resolution TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()