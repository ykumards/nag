import pytest
from datetime import datetime
from unittest.mock import patch
from nag.core import add_task, annotate_task, show_timeline

# Mock data for tasks
mock_tasks = [
    (1, "09:00", "10:00", "Task 1", "upcoming", None),
    (2, "10:00", "11:00", "Task 2", "upcoming", "Annotation 2")
]

@patch('nag.core.insert_task')
@patch('nag.core.console.print')
def test_add_task(mock_print, mock_insert_task):
    """Test adding a task successfully."""
    # Pass "today" (the human-readable string) to trigger the correct logic in `add_task`
    add_task("09:00", "10:00", "Test Task", "today")

    # Ensure the task was inserted into the DB
    mock_insert_task.assert_called_once()

    # Verify the correct message was printed (including the dynamically generated date)
    today = datetime.now().strftime("%Y-%m-%d")
    mock_print.assert_called_with(f"[green]Task added:[/green] Test Task from 09:00 to 10:00 on {today}")

@patch('nag.core.insert_task')
@patch('nag.core.console.print')
def test_add_task_past_date(mock_print, mock_insert_task):
    """Test adding a task with a past date (should fail)."""
    add_task("09:00", "10:00", "Test Task", "yesterday")
    mock_insert_task.assert_not_called()  # Ensure the task is NOT added
    mock_print.assert_called_with("[red]Error:[/red] You can only schedule tasks for today or future dates!")

@patch('nag.core.update_task_annotation')
@patch('nag.core.console.print')
def test_annotate_task(mock_print, mock_update_annotation):
    """Test annotating a task by row ID."""
    # Test successful annotation
    mock_update_annotation.return_value = True
    annotate_task(1, "New Annotation")
    mock_update_annotation.assert_called_once_with(1, "New Annotation")
    mock_print.assert_called_with("[cyan]Task with ID 1 annotated:[/cyan] New Annotation")

    # Test annotation failure (no task with given row ID)
    mock_update_annotation.return_value = False
    annotate_task(999, "Annotation")
    mock_print.assert_called_with("[red]No task found with ID 999")

@patch('nag.core.fetch_tasks_by_date')
@patch('nag.core.console.print')
def test_show_timeline(mock_print, mock_fetch_tasks):
    """Test showing the timeline for a specific date."""
    # Mock the tasks to be returned for the specific date
    mock_fetch_tasks.return_value = mock_tasks

    today = datetime.now().strftime("%Y-%m-%d")
    show_timeline("today")
    mock_fetch_tasks.assert_called_once_with(today)
    assert mock_print.called