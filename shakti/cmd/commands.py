import sys
import yaml
from os.path import expandvars, join
from importlib import resources
from shakti.cmd.cmd_list import list_file
from shakti.utils import register_help, register_command
from shakti.cmd.cmd_list_eval import cmd_list_eval


@register_help("cmd")
def cmd(args):
    """Command-related utilities

    List of subcommands:
    - s cmd list
    - s cmd list-eval

    For more information on any subcommand, use --help flag.
    s --help cmd list
    s --help cmd list-eval
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

    if subcommand == "list":
        list_command()
    elif subcommand == "list-eval":
        list_eval_command()
    else:
        print(f"Error: Unknown subcommand '{subcommand}'")
        sys.exit(1)


@register_command("cmd list")
def list_command():
    """Display the contents of the curated commands file."""
    # Get the config file path from the Shakti package
    shakti_package = resources.files("shakti")
    config_path = join(shakti_package, "config.shakti.yaml")

    # Read the config file
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    # Get the file path from the config and expand environment variables
    file_path = expandvars(config["cmd"]["file_path"])

    # List the contents of the file
    list_file(file_path)


@register_command("cmd list-eval")
def list_eval_command():
    """Display the contents of the curated commands file."""
    # Get the config file path from the Shakti package
    shakti_package = resources.files("shakti")
    config_path = join(shakti_package, "config.shakti.yaml")

    # Read the config file
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    # Get the file path from the config and expand environment variables
    file_path = expandvars(config["cmd"]["file_path"])

    # List the contents of the file
    cmd_list_eval(file_path)
