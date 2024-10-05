import subprocess
import sys
import os
from shakti.utils import register_help


@register_help("git difftool")
def git_difftool(git_options, subcommand_args):
    """
    Run git difftool with .gitdiffignore support.

    This command runs git difftool but ignores files and folders specified in .gitdiffignore.
    All options and arguments are passed directly to git diff.

    ok

    Usage: s git [git options] difftool [options] [<commit>] [--] [<path>...]
    """

    def is_ignored(file_path):
        if os.path.exists(".gitdiffignore"):
            with open(".gitdiffignore", "r") as f:
                patterns = f.read().splitlines()
            for pattern in patterns:
                if file_path == pattern or file_path.startswith(pattern + os.sep):
                    return True
        return False

    # Get the list of changed files
    try:
        changed_files = subprocess.check_output(
            ["git"] + ["diff", "--name-only"] + subcommand_args, universal_newlines=True
        ).splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error executing git diff: {e}", file=sys.stderr)
        sys.exit(e.returncode)

    # Filter out ignored files
    filtered_files = [file for file in changed_files if not is_ignored(file)]

    if filtered_files:
        # Run git difftool with filtered files
        try:
            subprocess.run(
                ["git"]
                + git_options
                + ["difftool"]
                + subcommand_args
                + ["--"]
                + filtered_files,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error executing git difftool: {e}", file=sys.stderr)
            sys.exit(e.returncode)
    else:
        print("No changes to display after applying .gitdiffignore")
