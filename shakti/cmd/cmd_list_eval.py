import sys
import yaml
import subprocess
from os.path import expandvars
from shakti.utils import register_help, register_command
import shlex
import readline


@register_help("cmd list-eval")
def cmd_list_eval(file_path):
    """
    List commands from the curated file, allow selection with fzf, and execute the selected command.

    Original command:
    selected_command=$(s cmd list | fzf | awk -F 'command: |\\|tags' '{print $2}') && vared -p "Edit and execute: " -c selected_command && eval "$selected_command"

    Usage:
        s cmd list-eval

    This command will:
    1. List available commands
    2. Allow selection using fzf
    3. Provide an opportunity to edit the selected command
    4. Execute the final command
    """
    # Get the list of commands
    commands = get_commands(file_path)

    # Use fzf for selection
    selected_command = fzf_select(commands)
    if not selected_command:
        print("No command selected.")
        return

    # Allow editing the selected command
    edited_command = edit_command(selected_command)

    # Execute the command
    execute_command(edited_command)


def get_commands(file_path):
    """Read commands from the specified file."""
    commands = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split("|")
                    if len(parts) >= 2:
                        command = parts[0].strip()
                        tags = "|".join(parts[1:]).strip()
                        commands.append(f"{command} |{tags}")
    except IOError as e:
        print(f"Error reading file: {e}")
    return commands


def fzf_select(commands):
    """Use fzf to select a command from the list."""
    try:
        process = subprocess.Popen(
            ["fzf"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, _ = process.communicate(input="\n".join(commands))
        if process.returncode == 0:
            selected = stdout.strip()
            if selected:
                # Extract only the command part
                command_part = selected.split("|tags")[0].strip()
                if command_part.startswith("command: "):
                    command_part = command_part[9:].strip()
                return command_part
    except Exception as e:
        print(f"Error during fzf selection: {e}")
    return None


def edit_command(command):
    """Allow the user to edit the selected command."""
    try:
        # Set up readline to use the command as the default input
        readline.set_startup_hook(lambda: readline.insert_text(command))
        try:
            # Use input() to allow editing the command
            edited_command = input(
                "Edit and execute (modify or press Enter to keep as is):\n> "
            ).strip()
        finally:
            # Reset the readline startup hook
            readline.set_startup_hook()
        return edited_command if edited_command else command
    except Exception as e:
        print(f"Error during command editing: {e}")
    return command


def execute_command(command):
    """Execute the given command."""
    try:
        # Remove any leading "command:" if present
        if command.startswith("command:"):
            command = command[8:].strip()

        # Use shlex.split to properly handle command arguments
        args = shlex.split(command)
        print(f"Executing: {command}")
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except FileNotFoundError as e:
        print(f"Command not found: {e}")
