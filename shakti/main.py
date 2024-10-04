import click
from shakti.bye import bye
from shakti.hello import hello


@click.group()
def cli():
    """Shakti CLI"""
    pass


cli.add_command(hello)
cli.add_command(bye)

if __name__ == "__main__":
    cli()
