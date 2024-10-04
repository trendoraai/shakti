import click
from functools import wraps


def list_commands(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    command = ctx.command
    parent = ctx.parent

    if parent:
        click.echo(f"Registered subcommands for {parent.command.name} {command.name}:")
    else:
        click.echo(f"Registered commands for {command.name}:")

    for cmd_name in sorted(command.commands):
        cmd = command.commands[cmd_name]
        click.echo(f"- {cmd_name}: {cmd.help}")
        if isinstance(cmd, click.Group) and not parent:
            for subcmd_name in sorted(cmd.commands):
                subcmd = cmd.commands[subcmd_name]
                click.echo(f"  - {cmd_name} {subcmd_name}: {subcmd.help}")
    ctx.exit()


def add_list_option(cmd):
    if isinstance(cmd, click.Command):
        cmd.params.append(
            click.Option(
                ("--shakti-list",),
                is_flag=True,
                callback=list_commands,
                expose_value=False,
                is_eager=True,
                help="List all registered commands and subcommands.",
            )
        )
        return cmd
    else:

        @wraps(cmd)
        def wrapper(*args, **kwargs):
            @click.option(
                "--shakti-list",
                is_flag=True,
                callback=list_commands,
                expose_value=False,
                is_eager=True,
                help="List all registered commands and subcommands.",
            )
            @wraps(cmd)
            def new_cmd(*args, **kwargs):
                return cmd(*args, **kwargs)

            return new_cmd(*args, **kwargs)

        return wrapper
