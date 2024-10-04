import click
import subprocess
from .git_add import git_add
from .git_message import git_message
from shakti.utils import list_commands


@click.group(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.option(
    "--shakti-list",
    is_flag=True,
    callback=list_commands,
    expose_value=False,
    is_eager=True,
    help="List all registered commands and subcommands.",
)
def git():
    """Git related commands

    List of subcommands:
    - s git add
    - s git message

    For more information on any subcommand, use --help flag.
    s git add --help
    """
    pass


@git.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def add(args):
    """Run black and then git add with given arguments."""
    git_add(args)


@git.command()
def message():
    """Generate an AI commit message and output the git commit command ready for execution."""
    git_message()


# Override the git group's invoke method to handle unregistered commands
def invoke(self, ctx):
    if "--shakti-list" in ctx.args:
        # Handle --shakti-list option
        list_commands(ctx, None, True)
    elif ctx.protected_args and ctx.protected_args[0] not in self.commands:
        # If the subcommand is not registered, treat it as a regular git command
        command = ["git"] + ctx.protected_args + ctx.args
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            click.echo(f"Error executing git command: {e}", err=True)
            ctx.exit(e.returncode)
    else:
        # For registered commands, use the default behavior
        super(click.Group, self).invoke(ctx)


git.invoke = invoke.__get__(git)
