from pathlib import Path


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
            return [
                line.strip()
                for line in f
                if line.strip() and not line.strip().startswith("#")
            ]
    return []
