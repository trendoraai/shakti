import click
import subprocess
from .git_add import git_add


@click.group(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True),
    invoke_without_command=True,
)
@click.pass_context
def git(ctx, *args, **kwargs):
    """Git related commands"""
    if ctx.invoked_subcommand is None:
        # If no subcommand is specified or the subcommand is not registered,
        # run git with all arguments
        command = ["git"] + list(ctx.args)
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            click.echo(f"Error executing git command: {e}", err=True)
            ctx.exit(e.returncode)
    else:
        # This block will be executed for registered subcommands
        pass


git.add_command(click.command()(git_add), name="add")


# Override the git group's invoke method to handle unregistered commands
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
