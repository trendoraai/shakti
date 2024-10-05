import click
import subprocess
import os


def git_add(args):
    """
    Run black formatter and then git add with given arguments.

    This command performs the following steps:
    1. Runs the 'black' formatter on the current directory.
    2. Adds files to the git staging area using the provided arguments.

    Usage:
        s git add [OPTIONS] [ARGS]...

    Examples:
        s git add .
        s git add file1.py file2.py

    Note:
        - The 'black' formatter is run using 'poetry run black .'
        - If 'black' fails, the git add operation will not proceed.
        - Any errors during 'black' or 'git add' will be reported.
    """
    click.echo("Shakti: Command found.")
    formatter = determine_formatter()

    if formatter:
        click.echo(f"Running {formatter['name']}...")
        try:
            subprocess.run(formatter["command"], check=True)
            click.echo(f"{formatter['name']} formatting complete.")
        except subprocess.CalledProcessError as e:
            click.echo(f"Error running {formatter['name']}: {e}")
            if click.confirm("Do you want to proceed with git add anyway?"):
                pass
            else:
                return
    else:
        click.echo("No suitable formatter found. Proceeding with git add.")

    click.echo("Adding files to staging area with arguments: " + " ".join(args))
    try:
        subprocess.run(["git", "add"] + list(args), check=True)
        click.echo("Files added to staging area.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error adding files: {e}")


def determine_formatter():
    """
    Determine the appropriate formatter based on project setup.
    """
    if os.path.exists("pyproject.toml"):
        if command_exists("poetry"):
            return {"name": "black", "command": ["poetry", "run", "black", "."]}
        elif command_exists("black"):
            return {"name": "black", "command": ["black", "."]}
    elif os.path.exists("package.json"):
        if command_exists("npx") and prettier_exists():
            return {"name": "prettier", "command": ["npx", "prettier", "--write", "."]}

    return None


def prettier_exists():
    """
    Check if Prettier is available in the project.
    """
    try:
        subprocess.run(
            ["npx", "--no-install", "prettier", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def command_exists(cmd):
    """
    Check if a command exists and is executable.
    """
    return (
        subprocess.call(
            ["which", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        == 0
    )
