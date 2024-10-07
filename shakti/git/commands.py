import sys
import subprocess
import os
from .git_add import git_add
from .git_message import git_message
from .git_diff import git_diff
from .git_difftool import git_difftool
from .git_tree import git_tree
from .git_signature import git_signature
from shakti.utils import register_help, register_command


@register_help("git")
def git(args):
    """Git related commands

    List of subcommands:
    - s git add
    - s git message
    - s git diff
    - s git difftool
    - s git tree
    - s git signature

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
    elif subcommand == "tree":
        tree(subcommand_args)
    elif subcommand == "signature":
        signature(subcommand_args)
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


@register_command("git tree")
def tree(subcommand_args):
    """Generate a tree-like representation of files in a Git repository."""
    git_tree(subcommand_args)


@register_command("git signature")
def signature(args):
    """Extract function and class signatures from Python files and folders."""
    retain_docstring = False
    retain_full_docstring = False
    paths = []

    for arg in args:
        if arg == "--retain-docstring":
            retain_docstring = True
        elif arg == "--retain-full-docstring":
            retain_full_docstring = True
        else:
            paths.append(arg)

    if not paths:
        print("Error: No files or folders specified.")
        print(signature.__doc__)
        return

    git_signature(paths, retain_docstring, retain_full_docstring)
