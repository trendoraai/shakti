import click
import subprocess


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
    click.echo("Running black...")
    try:
        subprocess.run(["poetry", "run", "black", "."], check=True)
        click.echo("Black formatting complete.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error running black: {e}")
        return

    click.echo("Adding files to staging area with arguments: " + " ".join(args))
    try:
        subprocess.run(["git", "add"] + list(args), check=True)
        click.echo("Files added to staging area.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error adding files: {e}")
