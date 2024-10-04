import click
from shakti.bye import bye
from shakti.hello import hello
from shakti.git.commands import git


@click.group()
def cli():
    """Shakti CLI"""
    pass


cli.add_command(hello)
cli.add_command(bye)
cli.add_command(git)

if __name__ == "__main__":
    cli()
