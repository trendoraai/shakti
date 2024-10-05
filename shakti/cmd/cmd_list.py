import os
from shakti.utils import register_help


@register_help("list")
def list_file(file_path):
    """
    Display the contents of a specified file.

    Usage:
        s list <file_path>

    Example:
        s list shakti/main.py
    """
    if not file_path:
        print("Error: Please provide a file path.")
        return

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        with open(file_path, "r") as file:
            print(f"Contents of {file_path}:")
            print("=" * 40)
            print(file.read())
            print("=" * 40)
    except IOError as e:
        print(f"Error reading file: {e}")
