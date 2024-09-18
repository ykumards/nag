import sqlite3
from pathlib import Path
from rich.console import Console
from rich.table import Table
from datetime import datetime

# Path to the .nag directory and the SQLite database
NAG_DIR = Path.home() / '.nag'
DB_FILE = NAG_DIR / 'nag_tasks.db'

# Ensure the directory and database are created
NAG_DIR.mkdir(exist_ok=True)

# SQLite database connection
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Create the tasks table if it doesn't exist
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
conn.commit()

console = Console()

def add_task(start_time, end_time, task_name):
    """Add a new task to the schedule."""
    date = datetime.now().strftime("%Y-%m-%d")  # Store the date of the task
    status = 'upcoming'
    c.execute('''
        INSERT INTO tasks (date, start_time, end_time, task_name, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, start_time, end_time, task_name, status))
    conn.commit()
    console.print(f"[green]Task added:[/green] {task_name} from {start_time} to {end_time} on {date}")

def annotate_task(start_time, end_time, annotation):
    """Annotate a task."""
    date = datetime.now().strftime("%Y-%m-%d")
    c.execute('''
        UPDATE tasks
        SET annotation = ?
        WHERE start_time = ? AND end_time = ? AND date = ?
    ''', (annotation, start_time, end_time, date))
    if c.rowcount > 0:
        conn.commit()
        console.print(f"[cyan]Task from {start_time} to {end_time} on {date} annotated:[/cyan] {annotation}")
    else:
        console.print(f"[red]No task found from {start_time} to {end_time} on {date}")

def show_timeline():
    """Show the current day's timeline, displaying only time blocks that have tasks."""
    date = datetime.now().strftime("%Y-%m-%d")  # Display tasks only for today
    now = datetime.now().strftime("%H:%M")

    # Fetch tasks for today
    c.execute('''
        SELECT start_time, end_time, task_name, status, annotation
        FROM tasks
        WHERE date = ?
        ORDER BY start_time
    ''', (date,))
    tasks = c.fetchall()

    # Display using Rich
    table = Table(title=f"Nag 🐍️ - Today's Schedule\n(Current Time: {now})")
    table.add_column("Time Block", justify="center", style="cyan")
    table.add_column("Task", justify="left", style="magenta")
    table.add_column("Status", justify="center", style="green")

    if not tasks:
        console.print("[yellow]No tasks scheduled for today.[/yellow]")
        return

    for task in tasks:
        start, end, task_name, status, annotation = task
        if start <= now <= end:
            status = "[bold green]In Progress[/bold green]"
        elif now > end:
            status = "[bold red]Overdue[/bold red]"
        else:
            status = "[yellow]Upcoming[/yellow]"

        table.add_row(f"{start} - {end}", task_name, status)

    console.print(table)

def cleanup():
    """Close the database connection when done."""
    conn.close()