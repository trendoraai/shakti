import subprocess
import os
import sys


def git_add(args):
    """
    Run black formatter and then git add with given arguments.

    This command performs the following steps:
    1. Runs the appropriate formatter on the current directory.
    2. Adds files to the git staging area using the provided arguments.

    Usage:
        s git add [OPTIONS] [ARGS]...

    Examples:
        s git add .
        s git add file1.py file2.py

    Note:
        - The formatter (black or prettier) is run if available
        - If the formatter fails, the git add operation will not proceed unless confirmed
        - Any errors during formatting or 'git add' will be reported.
    """
    print("Shakti: Command found.")
    formatter = determine_formatter()

    if formatter:
        print(f"Running {formatter['name']}...")
        try:
            subprocess.run(formatter["command"], check=True)
            print(f"{formatter['name']} formatting complete.")
        except subprocess.CalledProcessError as e:
            print(f"Error running {formatter['name']}: {e}")
            if (
                input("Do you want to proceed with git add anyway? (y/N) ").lower()
                != "y"
            ):
                return
    else:
        print("No suitable formatter found. Proceeding with git add.")

    print("Adding files to staging area with arguments: " + " ".join(args))
    try:
        subprocess.run(["git", "add"] + args, check=True)
        print("Files added to staging area.")
    except subprocess.CalledProcessError as e:
        print(f"Error adding files: {e}", file=sys.stderr)


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
