from pathlib import Path

from db import get_db_connection

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_FILE = BASE_DIR / "schema.sql"
SEED_FILE = BASE_DIR / "seed.sql"


def run_sql_file(cursor, file_path: Path) -> None:
    sql_content = file_path.read_text(encoding="utf-8")
    cursor.execute(sql_content)


def initialize_database() -> None:
    conn = get_db_connection()
    try:
        conn.autocommit = False
        with conn.cursor() as cursor:
            run_sql_file(cursor, SCHEMA_FILE)
            run_sql_file(cursor, SEED_FILE)
        conn.commit()
        print("Database initialized successfully: schema created and seed data inserted.")
    except Exception as exc:
        conn.rollback()
        raise RuntimeError(f"Database initialization failed: {exc}") from exc
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()
