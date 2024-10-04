import click


@click.command(help="Say hello from Shakti")
def hello():
    """A simple program that says hello."""
    click.echo("Hello from Shakti!")
