import click
from functools import wraps

# Initialize COMMANDS and SHAKTI_OPTIONS
COMMANDS = {}
SHAKTI_OPTIONS = {}


def register_command(func):
    """Decorator to register commands"""
    name = func.__name__
    COMMANDS[name] = {
        "function": func,
        "description": func.__doc__ or "No description provided",
        "options": getattr(func, "options", []),
    }
    return func


def register_option(func):
    """Decorator to register shakti options"""
    name = f"--{func.__name__.replace('_', '-')}"
    SHAKTI_OPTIONS[name] = {
        "function": func,
        "description": func.__doc__ or "No description provided",
    }
    return func


def command_option(name, description):
    """Decorator to register command-specific options"""

    def decorator(func):
        if not hasattr(func, "options"):
            func.options = []
        func.options.append((name, description))
        return func

    return decorator


@register_option
def slist():
    """List all available commands and shakti options"""
    print("Available commands:")
    for name, info in COMMANDS.items():
        print(f"  {name:<10} {info['description']}")
        for opt, opt_desc in info["options"]:
            print(f"    {opt:<12} {opt_desc}")
    print("\nShakti options:")
    for opt, info in SHAKTI_OPTIONS.items():
        print(f"  {opt:<12} {info['description']}")


def show_command_help(command):
    if command in COMMANDS:
        info = COMMANDS[command]
        print(f"{command} - {info['description']}")
        if info["options"]:
            print("Options:")
            for opt, opt_desc in info["options"]:
                print(f"  {opt:<12} {opt_desc}")
    else:
        print(f"Unknown command: {command}")


def shelp():
    print("Shakti CLI")
    print("\nUsage: shakti [options] <command> [options] <subcommand> [args...]")
    print("\nShakti options:")
    for opt, info in SHAKTI_OPTIONS.items():
        print(f"  {opt:<12} {info['description']}")
    print("\nAvailable commands:")
    for name, info in COMMANDS.items():
        print(f"  {name:<10} {info['description']}")
    print("\nUse 'shakti --help <command>' for more information about a command.")
