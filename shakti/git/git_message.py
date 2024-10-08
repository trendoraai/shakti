import subprocess
import shlex
import sys
from shakti.utils import register_help
from shakti.git.utils import is_ignored, get_ignore_patterns


@register_help("git message")
def git_message():
    """
    Generate an AI commit message and output the git commit command ready for execution.

    This function performs the following steps:
    1. Retrieves the last two commit messages from the git log.
    2. Gets the staged changes using git diff.
    3. Sends this information to an AI model to generate a commit message.
    4. Displays the AI-generated commit message.
    5. Outputs a git commit command with the generated message, ready for execution.

    Usage:
        This function is typically called by a CLI command, e.g., 's git message'

    Note:
        - The function uses 'aichat' to generate the commit message.
        - It follows Conventional Commit guidelines.
        - If there's an error generating the message, it will be reported to stderr.
        - The commit message is properly escaped for shell use.

    Returns:
        None. The function prints the results to stdout.
    """

    # Get the list of staged files
    try:
        staged_files = subprocess.check_output(
            ["git", "diff", "--staged", "--name-only"], universal_newlines=True
        ).splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error getting staged files: {e}", file=sys.stderr)
        return

    # Get ignore patterns
    ignore_patterns = get_ignore_patterns()

    # Filter out ignored files
    filtered_files = [
        file for file in staged_files if not is_ignored(file, ignore_patterns)
    ]

    if not filtered_files:
        print("No changes to commit after applying .gitdiffignore", file=sys.stderr)
        return

    # Generate AI commit message
    ai_commit_command = [
        "bash",
        "-c",
        f"""{{ echo "Give commit message for the following changes, follow Conventional Commit guidelines. \n\nHere are examples of couple of commit messages for your reference: \nExample one and two:\n" ; git --no-pager log -2 --pretty=format:"%B"; echo "\n\nAnd now here are the diffs: "; git --no-pager diff --staged -- {' '.join(shlex.quote(f) for f in filtered_files)}; }} | aichat""",
    ]

    try:
        ai_commit_message = subprocess.check_output(
            ai_commit_command, text=True, stderr=subprocess.PIPE
        ).strip()
        print("AI Commit Message:\n\n")
        print(ai_commit_message)
    except subprocess.CalledProcessError as e:
        print(f"Error generating AI commit message: {e}", file=sys.stderr)
        print(f"Error output: {e.stderr.decode()}", file=sys.stderr)
        return

    # Escape the commit message for shell
    escaped_message = shlex.quote(ai_commit_message)

    # Output the git commit command directly
    print("\n\nCommit command:\n\n")
    print(f"git commit -m {escaped_message}", end="")
