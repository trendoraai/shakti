import os
from shakti.utils import register_help


@register_help("cmd list")
def list_file(file_path):
    """
    Display the contents of curated commands file.
    You can define the file path in the config.shakti.yaml file.

    Usage:
        s cmd list

    Example:
        s cmd list
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
