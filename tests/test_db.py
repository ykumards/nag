import pytest
import sqlite3
from nag.db import get_db_connection, insert_task, update_task_annotation, fetch_tasks_by_date

# Mock the DB file path to use an in-memory database for testing
@pytest.fixture
def in_memory_db():
    """Fixture to provide a fresh in-memory database for each test."""
    with sqlite3.connect(":memory:") as conn:
        c = conn.cursor()

        # Create the tasks table in the in-memory database
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
        yield conn, c  # Provide the connection and cursor to the test
        conn.commit()


def test_insert_task(in_memory_db):
    """Test inserting a task into the database."""
    conn, c = in_memory_db

    # Insert a task
    insert_task("2024-09-19", "09:00", "10:00", "Test Task", "upcoming", connection=(conn, c))

    # Check if the task was inserted
    c.execute("SELECT * FROM tasks WHERE task_name = ?", ("Test Task",))
    result = c.fetchone()

    assert result is not None
    assert result[4] == "Test Task"
    assert result[1] == "2024-09-19"
    assert result[5] == "upcoming"


def test_update_task_annotation(in_memory_db):
    """Test updating a task annotation."""
    conn, c = in_memory_db

    # Insert a task first
    insert_task("2024-09-19", "09:00", "10:00", "Test Task", "upcoming", connection=(conn, c))

    # Fetch the task's rowid
    c.execute("SELECT id FROM tasks WHERE task_name = ?", ("Test Task",))
    rowid = c.fetchone()[0]

    # Update the task annotation
    assert update_task_annotation(rowid, "New Annotation", connection=(conn, c)) is True

    # Verify the annotation was updated
    c.execute("SELECT annotation FROM tasks WHERE id = ?", (rowid,))
    annotation = c.fetchone()[0]

    assert annotation == "New Annotation"


def test_fetch_tasks_by_date(in_memory_db):
    """Test fetching tasks by date."""
    conn, c = in_memory_db

    # Insert multiple tasks with different dates
    insert_task("2024-09-19", "09:00", "10:00", "Task 1", "upcoming", connection=(conn, c))
    insert_task("2024-09-19", "10:00", "11:00", "Task 2", "upcoming", connection=(conn, c))
    insert_task("2024-09-20", "11:00", "12:00", "Task 3", "upcoming", connection=(conn, c))

    # Fetch tasks for a specific date
    tasks = fetch_tasks_by_date("2024-09-19", connection=(conn, c))

    # Verify that the correct tasks were fetched
    assert len(tasks) == 2
    assert tasks[0][3] == "Task 1"
    assert tasks[1][3] == "Task 2"

    # Ensure tasks for another date are fetched separately
    tasks = fetch_tasks_by_date("2024-09-20", connection=(conn, c))
    assert len(tasks) == 1
    assert tasks[0][3] == "Task 3"