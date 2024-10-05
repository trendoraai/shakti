import sys
import yaml
from os.path import expandvars
from .cmd_list import list_file
from shakti.utils import register_help, register_command
from .cmd_list_eval import cmd_list_eval


@register_help("cmd")
def cmd(args):
    """Command-related utilities

    List of subcommands:
    - s cmd list
    - s cmd list-eval

    For more information on any subcommand, use --help flag.
    s cmd --help list
    s cmd --help list-eval
    """
    if not args:
        print(cmd.__doc__)
        return

    cmd_options = []
    while args and (args[0].startswith("-") or args[0].startswith("--")):
        cmd_options.append(args.pop(0))

    if not args:
        print("Error: Please specify a subcommand.")
        return

    subcommand = args[0]
    subcommand_args = args[1:]

    if subcommand == "list":
        list_command(cmd_options + subcommand_args)
    elif subcommand == "list-eval":
        list_eval_command(cmd_options + subcommand_args)
    else:
        print(f"Error: Unknown subcommand '{subcommand}'")
        sys.exit(1)


@register_command("cmd list")
def list_command(args):
    """Display the contents of the curated commands file."""
    # Read the config file
    with open("config.shakti.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    # Get the file path from the config and expand environment variables
    file_path = expandvars(config["cmd"]["file_path"])

    # List the contents of the file
    list_file(file_path)


@register_command("cmd list-eval")
def list_eval_command(args):
    """Display the contents of the curated commands file."""
    # Read the config file
    with open("config.shakti.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    # Get the file path from the config and expand environment variables
    file_path = expandvars(config["cmd"]["file_path"])

    # List the contents of the file
    cmd_list_eval(file_path)
