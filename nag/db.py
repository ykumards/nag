import sqlite3
from pathlib import Path

# Path to the .nag directory and the SQLite database
NAG_DIR = Path.home() / '.nag'
DB_FILE = NAG_DIR / 'nag_tasks.db'

# Ensure the directory and database are created
NAG_DIR.mkdir(exist_ok=True)


def get_db_connection():
    """Get the SQLite database connection."""
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
    return conn, c


def get_connection_or_default(connection):
    """Return the provided connection or create a new one."""
    if connection:
        return connection, False  # Return connection and `False` to indicate it's not a new one
    else:
        return get_db_connection(), True  # Return new connection and `True`


def insert_task(date, start_time, end_time, task_name, status, connection=None):
    """Insert a new task into the database, optionally using a passed connection."""
    (conn, c), close_connection = get_connection_or_default(connection)

    try:
        c.execute('''
            INSERT INTO tasks (date, start_time, end_time, task_name, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, start_time, end_time, task_name, status))
    finally:
        if close_connection:
            conn.commit()
            conn.close()


def update_task_annotation(row_id, annotation, connection=None):
    """Update task annotation by row ID, optionally using a passed connection."""
    (conn, c), close_connection = get_connection_or_default(connection)

    try:
        c.execute('''
            UPDATE tasks
            SET annotation = ?
            WHERE rowid = ?
        ''', (annotation, row_id))
        return c.rowcount > 0
    finally:
        if close_connection:
            conn.commit()
            conn.close()


def fetch_tasks_by_date(date, connection=None):
    """Fetch tasks for a specific date, optionally using a passed connection."""
    (conn, c), close_connection = get_connection_or_default(connection)

    try:
        c.execute('''
            SELECT rowid, start_time, end_time, task_name, status, annotation
            FROM tasks
            WHERE date = ?
            ORDER BY start_time
        ''', (date,))
        return c.fetchall()
    finally:
        if close_connection:
            conn.close()