# nag 🐍️

**nag** is a command-line time-blocking tool designed to help you organize your day with time blocks. Add tasks to your schedule, annotate them, and display your timeline — all from the terminal.

## Features

- Add time blocks for specific tasks.
- Annotate existing time blocks.
- Display your timeline for a given day.
- Simple and intuitive command-line interface.

## Installation

#### 1. Using pipx (recommended)

pipx is a great tool for installing Python applications in isolated environments, so you don’t clutter your global Python installation.

To install pipx:
```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

After you have pipx installed, you can install nag:

```bash
pipx install nag
```

This will install nag and ensure it’s available globally on your system.

#### 2. Using pip

You can also install nag using pip if you prefer to install it directly into your Python environment.

```bash
pip install nag
```

## Usage

#### 1. Adding a Time Block

To add a new task to your schedule:

```bash
nag block 09:00 10:00 "Meeting with team"
```

This will add a task from 9:00 AM to 10:00 AM with the description "Meeting with team" for today by default. You can also specify a date:

```bash
nag block 09:00 10:00 "Meeting with team" --task-date 09/19
```

#### 2. Annotating a task

To annotate an existing task using its ID (as shown in the timeline):

```bash
nag annotate <task_id> "Discussed project progress."
```

#### 3. Showing your schedule

To view your schedule for today:

```bash
nag show
```

You can also show the schedule for a specific date:

```bash
nag show --date 09/19
```

#### Help

You can get help for any command by running:

```bash
nag --help
```

```
Usage: nag [OPTIONS] COMMAND [ARGS]...

  nag 🐍️ - Command-line time-blocking tool.

Options:
  --help  Show this message and exit.

Commands:
  annotate  Annotate an existing time block using its ID.
  block     Add a time block to your schedule with an optional date.
  show      Show the timeline for the given date.
```

For specific commands, such as block or show, you can also run:

```bash
nag block --help
nag show --help
```

## Contributing

Contributions are welcome! If you’d like to contribute to this project, feel free to open a pull request or submit an issue.

## License
This project is licensed under the MIT License.