import sqlite3
from pathlib import Path
from contextlib import contextmanager

# Path to the .nag directory and the SQLite database
NAG_DIR = Path.home() / '.nag'
DB_FILE = NAG_DIR / 'nag_tasks.db'

# Ensure the directory and database are created
NAG_DIR.mkdir(exist_ok=True)

@contextmanager
def get_db_connection():
    """Context manager for SQLite database connection and cursor with table creation check."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Ensure the 'tasks' table is created on the first run
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            task_name TEXT NOT NULL,
            status TEXT NOT NULL,
            annotation TEXT
        )
    ''')

    try:
        yield conn, c  # Provide the connection and cursor to the calling function
    finally:
        conn.commit()  # Commit the changes (if any)
        conn.close()  # Ensure the connection is always closed


def insert_task(date, start_time, end_time, task_name, status, connection=None):
    """Insert a new task into the database, optionally using a passed connection."""
    conn, c = connection if connection else get_db_connection()
    with conn:
        c.execute('''
            INSERT INTO tasks (date, start_time, end_time, task_name, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, start_time, end_time, task_name, status))


def update_task_annotation(row_id, annotation, connection=None):
    """Update task annotation by row ID, optionally using a passed connection."""
    conn, c = connection if connection else get_db_connection()
    with conn:
        c.execute('''
            UPDATE tasks
            SET annotation = ?
            WHERE rowid = ?
        ''', (annotation, row_id))
        return c.rowcount > 0


def fetch_tasks_by_date(date, connection=None):
    """Fetch tasks for a specific date, optionally using a passed connection."""
    conn, c = connection if connection else get_db_connection()
    with conn:
        c.execute('''
            SELECT rowid, start_time, end_time, task_name, status, annotation
            FROM tasks
            WHERE date = ?
            ORDER BY start_time
        ''', (date,))
        return c.fetchall()