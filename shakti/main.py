import click
import subprocess
from shakti.bye import bye
from shakti.hello import hello
from shakti.git.commands import git
from shakti.utils import add_list_option, list_commands


@click.group(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
@click.option(
    "--shakti-list",
    is_flag=True,
    callback=list_commands,
    expose_value=False,
    is_eager=True,
    help="List all registered commands and subcommands.",
)
def cli(ctx):
    """Shakti CLI"""
    pass


cli.add_command(hello)
cli.add_command(bye)
cli.add_command(git)


# Override the cli group's invoke method to handle unregistered commands
def invoke(self, ctx):
    if "--shakti-list" in ctx.args:
        # Handle --shakti-list option
        list_commands(ctx, None, True)
    elif ctx.protected_args and ctx.protected_args[0] not in self.commands:
        # If the command is not registered, treat it as a system command
        command = ctx.protected_args + ctx.args
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            click.echo(f"Error executing command: {e}", err=True)
            ctx.exit(e.returncode)
        except FileNotFoundError:
            click.echo(f"Command not found: {command[0]}", err=True)
            ctx.exit(1)
    else:
        # For registered commands, use the default behavior
        super(click.Group, self).invoke(ctx)


cli.invoke = invoke.__get__(cli)

if __name__ == "__main__":
    cli()
