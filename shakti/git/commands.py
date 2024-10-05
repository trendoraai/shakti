import sys
import subprocess
from .git_add import git_add
from .git_message import git_message
from .git_diff import git_diff
from .git_difftool import git_difftool
from shakti.utils import register_help, register_command


@register_help("git")
def git(args):
    """Git related commands

    List of subcommands:
    - s git add
    - s git message
    - s git diff

    For more information on any subcommand, use --help flag.
    s --help git add
    """
    if not args:
        print(git.__doc__)
        return

    git_options = []
    while args and (args[0].startswith("-") or args[0].startswith("--")):
        git_options.append(args.pop(0))

    if not args:
        # If only options were provided, pass them to git
        command = ["git"] + git_options
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing git command: {e}", file=sys.stderr)
            sys.exit(e.returncode)
        return

    subcommand = args[0]
    subcommand_args = args[1:]

    if subcommand == "add":
        add(git_options + subcommand_args)
    elif subcommand == "message":
        message()
    elif subcommand == "diff":
        diff(git_options, subcommand_args)
    elif subcommand == "difftool":
        difftool(git_options, subcommand_args)
    else:
        # If the subcommand is not registered, treat it as a regular git command
        command = ["git"] + git_options + [subcommand] + subcommand_args
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing git command: {e}", file=sys.stderr)
            sys.exit(e.returncode)


@register_command("git add")
def add(args):
    """Run black and then git add with given arguments."""
    git_add(args)


@register_command("git message")
def message():
    """Generate an AI commit message and output the git commit command ready for execution."""
    git_message()


@register_command("git diff")
def diff(git_options, subcommand_args):
    """Run git diff with .gitdiffignore support."""
    git_diff(git_options, subcommand_args)


@register_command("git difftool")
def difftool(git_options, subcommand_args):
    """Run git difftool with .gitdiffignore support."""
    git_difftool(git_options, subcommand_args)
