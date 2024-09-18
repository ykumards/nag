import click
from .core import add_task, annotate_task, show_timeline

@click.group()
def nag():
    """Nag - Command-line time-blocking and productivity tool."""
    pass

@nag.command()
@click.argument('start_time')
@click.argument('end_time')
@click.argument('task_name')
@click.argument('task_date', required=False, default="today")
def block(start_time, end_time, task_name, task_date):
    """Add a time block to your schedule with an optional date (default: today)."""
    add_task(start_time, end_time, task_name, task_date)

@nag.command()
@click.argument('row_id')
@click.argument('annotation')
def annotate(row_id, annotation):
    """Annotate an existing time block using its ID."""
    annotate_task(row_id, annotation)

@nag.command()
@click.argument('date', required=False, default="today")
def show(date):
    """Show the timeline for the given date (default: today)."""
    show_timeline(date)

if __name__ == "__main__":
    nag()