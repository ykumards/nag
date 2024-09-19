import click
from .core import add_task, annotate_task, show_timeline

@click.group()
def nag():
    """nag 🐍️ - Command-line time-blocking tool."""
    pass

@nag.command()
@click.argument('start_time', metavar='<start_time>')
@click.argument('end_time', metavar='<end_time>')
@click.argument('task_name', metavar='<task_name>')
@click.option(
    '--task-date',
    default="today",
    show_default=True,
    metavar='<task_date>',
    help="The date for the task (optional, defaults to 'today'). Format: 'MM/DD', 'DD/MM', or 'today', 'tomorrow'.",
)
def block(start_time, end_time, task_name, task_date):
    """Add a time block to your schedule with an optional date."""
    add_task(start_time, end_time, task_name, task_date)

@nag.command()
@click.argument('row_id', metavar='<row_id>')
@click.argument('annotation', metavar='<annotation>')
def annotate(row_id, annotation):
    """Annotate an existing time block using its ID."""
    annotate_task(row_id, annotation)

@nag.command()
@click.option(
    '--date',
    default="today",
    show_default=True,
    metavar='<date>',
    help="The date for the schedule (optional, defaults to 'today'). Format: 'MM/DD', 'DD/MM', or 'today', 'yesterday', 'tomorrow'.",
)
def show(date):
    """Show the timeline for the given date."""
    show_timeline(date)

if __name__ == "__main__":
    nag()