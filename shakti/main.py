import sys
import subprocess
from shakti.bye import bye
from shakti.hello import hello
from shakti.git.commands import git
from shakti.cmd.commands import cmd
from shakti.utils import slist, shelp, HELP_REGISTRY
from shakti.report.commands import report


def cli():
    """Shakti CLI"""
    args = sys.argv[1:]
    if not args:
        print("Usage: shakti [options] <command> [options] <subcommand> [args...]")
        sys.exit(1)

    shakti_options = []
    while args and (args[0].startswith("-") or args[0].startswith("--")):
        shakti_options.append(args.pop(0))

    if "--version" in shakti_options:
        print("Shakti CLI version 1.0")  # Replace with actual version
        sys.exit(0)

    try:
        command = args.pop(0)
    except IndexError:
        command = ""

    if "--help" in shakti_options:
        if command:
            help_identifier = f"{command} {' '.join(args)}".strip()
            shelp(help_identifier)
        else:
            shelp()
        sys.exit(0)

    if "--slist" in shakti_options and command == "":
        slist()
        sys.exit(0)

    if command == "hello":
        hello(args)
    elif command == "bye":
        bye(args)
    elif command == "git":
        git(args)
    elif command == "cmd":
        cmd(args)
    elif command == "report":
        report(args)
    else:
        # If the command is not registered, treat it as a system command
        try:
            subprocess.run([command] + args, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}", file=sys.stderr)
            sys.exit(e.returncode)
        except FileNotFoundError:
            print(f"Command not found: {command}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    cli()
