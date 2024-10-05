import subprocess
import sys
from shakti.utils import register_help
from shakti.git.utils import is_ignored, get_ignore_patterns


@register_help("git diff")
def git_diff(git_options, subcommand_args):
    """
    Run git diff with .gitdiffignore support.

    This command runs git diff but ignores files and folders specified in .gitdiffignore.
    All options and arguments are passed directly to git diff.

    Usage: s git [git options] diff [options] [<commit>] [--] [<path>...]
    """

    # Get the list of changed files
    try:
        changed_files = subprocess.check_output(
            ["git"] + ["diff", "--name-only"] + subcommand_args, universal_newlines=True
        ).splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error executing git diff: {e}", file=sys.stderr)
        sys.exit(e.returncode)

    # Get ignore patterns
    ignore_patterns = get_ignore_patterns()

    # Filter out ignored files
    filtered_files = [
        file for file in changed_files if not is_ignored(file, ignore_patterns)
    ]

    if filtered_files:
        # Run git diff with filtered files
        try:
            subprocess.run(
                ["git"]
                + git_options
                + ["diff"]
                + subcommand_args
                + ["--"]
                + filtered_files,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error executing git diff: {e}", file=sys.stderr)
            sys.exit(e.returncode)
    else:
        print("No changes to display after applying .gitdiffignore")
