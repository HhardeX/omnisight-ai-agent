
from pathlib import Path
import sqlite3


DATABASE_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "omnisight.db"
)


def get_connection() -> sqlite3.Connection:
    """Return a connection to the OmniSight SQLite database."""

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        DATABASE_PATH,
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    """Create OmniSight persistence tables if they do not already exist."""

    connection = get_connection()

    try:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS browser_results (
                job_id TEXT NOT NULL,
                target_url TEXT NOT NULL,
                viewport TEXT NOT NULL,
                screenshot_path TEXT NOT NULL,
                dom_snapshot TEXT NOT NULL,
                element_bounds TEXT NOT NULL,
                PRIMARY KEY (job_id, viewport)
            );

            CREATE TABLE IF NOT EXISTS visual_results (
                job_id TEXT NOT NULL,
                target_url TEXT NOT NULL,
                viewport TEXT NOT NULL,
                defects TEXT NOT NULL,
                PRIMARY KEY (job_id, viewport)
            );

            CREATE TABLE IF NOT EXISTS published_repairs (
                job_id TEXT NOT NULL,
                viewport TEXT NOT NULL,
                branch_name TEXT NOT NULL,
                commit_sha TEXT NOT NULL,
                pull_request_url TEXT NOT NULL,
                PRIMARY KEY (job_id, viewport)
            );

            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                repository TEXT NOT NULL,
                commit_sha TEXT NOT NULL,
                branch TEXT NOT NULL,
                target_url TEXT NOT NULL,
                status TEXT NOT NULL,
                error_message TEXT,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT
            );
            """
        )

        connection.commit()
    finally:
        connection.close()

