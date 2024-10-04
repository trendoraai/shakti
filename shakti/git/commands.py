import click
import subprocess
from .git_add import git_add


@click.group(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
def git():
    """Git related commands"""
    pass


@git.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option("--help", is_flag=True, help="Show this message and exit.")
def add(args, help):
    """Run black and then git add with given arguments."""
    if help:
        ctx = click.get_current_context()
        ctx.info_name = "git add"
        click.echo(git_add.__doc__)
        ctx.exit()
    git_add(args)


# The custom invoke method remains the same
def invoke(self, ctx):
    if ctx.protected_args and ctx.protected_args[0] not in self.commands:
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
