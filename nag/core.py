from datetime import datetime
from rich.console import Console
from rich.table import Table

from .db import insert_task, update_task_annotation, fetch_tasks_by_date
from .helpers import parse_date

console = Console()

def validate_date(task_date):
    """Validate if the task date is in the future or today."""
    date = parse_date(task_date)
    if not date:
        console.print(f"[red]Invalid date format![/red] Use MM/DD, DD/MM, or 'today', 'yesterday', 'tomorrow'.")
        return None
    today = datetime.now().strftime("%Y-%m-%d")
    if date < today:
        console.print(f"[red]Error:[/red] You can only schedule tasks for today or future dates!")
        return None
    return date

def add_task(start_time, end_time, task_name, task_date="today"):
    """Add a new task to the schedule, with an optional future date (default: today)."""
    date = validate_date(task_date)
    if not date:
        return

    # Add the task to the database
    insert_task(date, start_time, end_time, task_name, "upcoming")
    console.print(f"[green]Task added:[/green] {task_name} from {start_time} to {end_time} on {date}")

def annotate_task(row_id, annotation):
    """Annotate a task by its row ID."""
    if update_task_annotation(row_id, annotation):
        console.print(f"[cyan]Task with ID {row_id} annotated:[/cyan] {annotation}")
    else:
        console.print(f"[red]No task found with ID {row_id}")

def show_timeline(date_input="today"):
    """Show the timeline for a specific date, defaulting to today if no date is specified."""
    date = parse_date(date_input)
    if not date:
        console.print(f"[red]Invalid date format![/red] Use MM/DD, DD/MM, or 'today', 'yesterday', 'tomorrow'.")
        return

    now = datetime.now().strftime("%H:%M")
    tasks = fetch_tasks_by_date(date)

    # Display using Rich
    table = Table(title=f"\nNag 🐍️ - Schedule for {date}\n(Current Time: {now})")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Time Block", justify="center", style="cyan")
    table.add_column("Task", justify="left", style="magenta")
    table.add_column("Status", justify="center", style="green")
    table.add_column("Notes", justify="left", style="dim cyan")

    if not tasks:
        console.print(f"[yellow]No tasks scheduled for {date}.[/yellow]")
        return

    for rowid, start, end, task_name, status, annotation in tasks:
        if start <= now <= end and date == datetime.now().strftime("%Y-%m-%d"):
            status = "[bold green]In Progress[/bold green]"
        elif now > end and date == datetime.now().strftime("%Y-%m-%d"):
            status = "[bold red]Overdue[/bold red]"
        else:
            status = "[yellow]Upcoming[/yellow]"

        table.add_row(f"{rowid}", f"{start} - {end}", task_name, status, annotation or "")

    console.print(table)