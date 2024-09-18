import sqlite3
from pathlib import Path
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
from contextlib import contextmanager

from .helpers import parse_date

# Path to the .nag directory and the SQLite database
NAG_DIR = Path.home() / '.nag'
DB_FILE = NAG_DIR / 'nag_tasks.db'

# Ensure the directory and database are created
NAG_DIR.mkdir(exist_ok=True)

console = Console()

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


def add_task(start_time, end_time, task_name, task_date="today"):
    """Add a new task to the schedule, with an optional future date (default: today)."""
    date = parse_date(task_date)  # Parse the provided date or use "tomorrow" as default

    if not date:
        console.print(f"[red]Invalid date format![/red] Use MM/DD, DD/MM, or 'tomorrow'.")
        return

    # Ensure the date is in the future
    today = datetime.now().strftime("%Y-%m-%d")
    if date < today:
        console.print(f"[red]Error:[/red] You can only schedule tasks for future dates!")
        return

    # Add the task to the database
    status = 'upcoming'
    with get_db_connection() as (conn, c):
        c.execute('''
            INSERT INTO tasks (date, start_time, end_time, task_name, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, start_time, end_time, task_name, status))

    console.print(f"[green]Task added:[/green] {task_name} from {start_time} to {end_time} on {date}")


def annotate_task(start_time, end_time, annotation):
    """Annotate a task."""
    date = datetime.now().strftime("%Y-%m-%d")
    with get_db_connection() as (conn, c):
        c.execute('''
            UPDATE tasks
            SET annotation = ?
            WHERE start_time = ? AND end_time = ? AND date = ?
        ''', (annotation, start_time, end_time, date))
        if c.rowcount > 0:
            console.print(f"[cyan]Task from {start_time} to {end_time} on {date} annotated:[/cyan] {annotation}")
        else:
            console.print(f"[red]No task found from {start_time} to {end_time} on {date}")


def show_timeline(date_input="today"):
    """Show the timeline for a specific date, defaulting to today if no date is specified."""
    date = parse_date(date_input)

    if not date:
        console.print(f"[red]Invalid date format![/red] Use MM/DD, DD/MM, or 'today', 'yesterday', 'tomorrow'.")
        return

    now = datetime.now().strftime("%H:%M")

    with get_db_connection() as (conn, c):
        # Fetch tasks for the specified date
        c.execute('''
            SELECT start_time, end_time, task_name, status, annotation
            FROM tasks
            WHERE date = ?
            ORDER BY start_time
        ''', (date,))
        tasks = c.fetchall()

    # Display using Rich
    table = Table(title=f"\nNag 🐍️ - Schedule for {date}\n(Current Time: {now})")
    table.add_column("Time Block", justify="center", style="cyan")
    table.add_column("Task", justify="left", style="magenta")
    table.add_column("Status", justify="center", style="green")

    if not tasks:
        console.print(f"[yellow]No tasks scheduled for {date}.[/yellow]")
        return

    for task in tasks:
        start, end, task_name, status, annotation = task
        if start <= now <= end and date == datetime.now().strftime("%Y-%m-%d"):
            status = "[bold green]In Progress[/bold green]"
        elif now > end and date == datetime.now().strftime("%Y-%m-%d"):
            status = "[bold red]Overdue[/bold red]"
        else:
            status = "[yellow]Upcoming[/yellow]"

        table.add_row(f"{start} - {end}", task_name, status)

    console.print(table)