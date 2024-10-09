import sys
import yaml
import os
from os.path import expandvars, join
from importlib import resources
from shakti.utils import register_help, register_command
from shakti.report.timer import main as timer_main, parse_timer_file, create_heatmap
from matplotlib.backends.backend_pdf import PdfPages


@register_help("report")
def report(args):
    """Report-related utilities

    List of subcommands:
    - s report timer [timer_file_path]

    For more information on any subcommand, use --help flag.
    s --help report timer
    """
    if not args:
        print(report.__doc__)
        return

    cmd_options = []
    while args and (args[0].startswith("-") or args[0].startswith("--")):
        cmd_options.append(args.pop(0))

    if not args:
        print("Error: Please specify a subcommand.")
        return

    subcommand = args.pop(0)

    if subcommand == "timer":
        timer_command(args)
    else:
        print(f"Error: Unknown subcommand '{subcommand}'")
        sys.exit(1)


@register_command("report timer")
def timer_command(args):
    """Generate a work activity heatmap based on the .timer file."""
    # Check if a timer file path is provided as an argument
    if args:
        timer_file_path = args[0]
    else:
        # If no argument is provided, check the config file in the Shakti package
        shakti_package = resources.files("shakti")
        config_path = join(shakti_package, "config.shakti.yaml")

        with open(config_path, "r") as config_file:
            config = yaml.safe_load(config_file)

        # Get the timer file path from the config and expand environment variables
        timer_file_path = expandvars(
            config.get("report", {}).get("timer_file_path", ".timer")
        )

    # If the path is not absolute, make it relative to the current directory
    if not os.path.isabs(timer_file_path):
        timer_file_path = os.path.join(os.getcwd(), timer_file_path)

    # Run the timer main function
    timer_main(timer_file_path)


# Add this function to the timer.py file
def main(timer_file_path):
    if not os.path.exists(timer_file_path):
        print(f"Error: {timer_file_path} not found.")
        return

    data = parse_timer_file(timer_file_path)
    fig = create_heatmap(data)

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "work_activity_heatmap.pdf")

    with PdfPages(output_path) as pdf:
        pdf.savefig(fig)

    print(f"Heatmap saved as: {os.path.abspath(output_path)}")
