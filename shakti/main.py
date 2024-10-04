import click
from shakti.bye import bye
from shakti.hello import hello
from shakti.git.git_add import git_add


@click.group()
def cli():
    """Shakti CLI"""
    pass


cli.add_command(hello)
cli.add_command(bye)
cli.add_command(git_add)

if __name__ == "__main__":
    cli()
