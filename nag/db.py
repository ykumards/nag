import sqlite3
from pathlib import Path
import yaml

# Path to the .nag directory and the SQLite database
NAG_DIR = Path.home() / '.nag'
CONFIG_FILE = NAG_DIR / 'nag.yaml'

default_config = {
    'database': {
        'name': 'nag_tasks.db',
        'location': str(NAG_DIR),
    }
}

def load_config():
    """Load the config file, create default config if it doesn't exist."""
    if not CONFIG_FILE.exists():
        # Create the .nag directory if it doesn't exist
        NAG_DIR.mkdir(exist_ok=True)

        # Write the default config to the nag.yaml file
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(default_config, f)

    # Load the config from the yaml file
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)

    return config

def get_db_path():
    """Get the full database path from the config."""
    config = load_config()

    # Combine the location and name of the database from the config
    db_location = Path(config['database']['location'])
    db_name = config['database']['name']

    return db_location / db_name


def get_db_connection():
    """Get the SQLite database connection using the path from the config."""
    db_file = get_db_path()

    # Ensure the .nag directory and database path exist
    db_file.parent.mkdir(exist_ok=True, parents=True)

    conn = sqlite3.connect(db_file)
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

def delete_task_by_id(row_id, connection=None):
    """Delete a task by its row ID, optionally using a passed connection."""
    (conn, c), close_connection = get_connection_or_default(connection)

    try:
        c.execute('DELETE FROM tasks WHERE rowid = ?', (row_id,))
        return c.rowcount > 0  # Return True if a row was deleted
    finally:
        if close_connection:
            conn.commit()
            conn.close()


def mark_task_done_by_id(row_id, connection=None):
    """Mark a task as done by its row ID."""
    (conn, c), close_connection = get_connection_or_default(connection)

    try:
        c.execute('''
            UPDATE tasks
            SET status = 'done'
            WHERE rowid = ?
        ''', (row_id,))
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