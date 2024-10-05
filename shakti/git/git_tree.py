import subprocess
import sys
from pathlib import Path
from shakti.git.utils import is_ignored, get_ignore_patterns
from shakti.utils import register_help


def build_tree(files):
    """Construct a nested dictionary representing the file tree structure."""
    tree = {}
    for file_path in files:
        parts = file_path.split("/")
        current = tree
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = None
    return tree


def print_tree(tree, prefix="", use_markdown=True):
    """Print the file tree structure."""
    items = list(tree.items())
    for i, (name, subtree) in enumerate(items):
        is_last_item = i == len(items) - 1
        if use_markdown:
            print(f"{prefix}- {name}")
            new_prefix = f"{prefix}  "
        else:
            connector = "└── " if is_last_item else "├── "
            print(f"{prefix}{connector}{name}")
            new_prefix = f"{prefix}{'    ' if is_last_item else '│   '}"

        if subtree is not None:
            print_tree(subtree, new_prefix, use_markdown)


@register_help("git tree")
def git_tree(subcommand_args):
    """
    Generate a tree-like representation of files in a Git repository.

    This command runs a tree-like representation of files, respecting .gitdiffignore.

    Usage: s git tree [options]

    Options:
      --complete    Include all files, ignoring .gitdiffignore
      --no-markdown Use ASCII characters instead of Markdown format
    """
    use_markdown = True
    skip_ignore = False

    for arg in subcommand_args:
        if arg == "--complete":
            skip_ignore = True
        elif arg == "--no-markdown":
            use_markdown = False

    try:
        files = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"], universal_newlines=True
        ).splitlines()

        if not skip_ignore:
            ignore_patterns = get_ignore_patterns()
            files = [f for f in files if not is_ignored(Path(f), ignore_patterns)]

        tree = build_tree(files)
        print_tree(tree, use_markdown=use_markdown)

    except subprocess.CalledProcessError as e:
        print(f"Error executing git ls-tree: {e}", file=sys.stderr)
        sys.exit(e.returncode)
