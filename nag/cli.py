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
def block(start_time, end_time, task_name):
    """Add a time block to your schedule."""
    add_task(start_time, end_time, task_name)

@nag.command()
@click.argument('start_time')
@click.argument('end_time')
@click.argument('annotation')
def annotate(start_time, end_time, annotation):
    """Annotate an existing time block."""
    annotate_task(start_time, end_time, annotation)

@nag.command()
def show():
    """Show the current day's timeline."""
    show_timeline()

if __name__ == "__main__":
    nag()