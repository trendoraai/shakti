import subprocess
import sys
from pathlib import Path
from shakti.utils import register_help, register_command


def is_ignored(file_path, ignore_patterns):
    path = Path(file_path)
    for pattern in ignore_patterns:
        if pattern.endswith("/"):
            # Directory pattern
            if path == Path(pattern[:-1]) or path.is_relative_to(pattern):
                return True
        else:
            # File pattern
            if path.match(pattern):
                return True
    return False


def get_ignore_patterns():
    ignore_file = Path(".gitdiffignore")
    if ignore_file.exists():
        with ignore_file.open() as f:
            return [line.strip() for line in f if line.strip()]
    return []


def build_tree(files):
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


def print_tree(tree, prefix="", is_last=True, use_markdown=True):
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
            print_tree(subtree, new_prefix, is_last_item, use_markdown)


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
